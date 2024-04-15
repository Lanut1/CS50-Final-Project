import os
import re
import uuid
import json


from cs50 import SQL
from functools import wraps
from flask import Flask, flash, redirect, render_template, abort, url_for, jsonify, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash


# Configure application
app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///project.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET"])
def index():
    """Display main page content"""
    posts = db.execute("SELECT image_path, id FROM posts")
    recipes = db.execute("SELECT image_path, id FROM recipes")
    return render_template("index.html", posts=posts, recipes=recipes)


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    session.clear()

    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            apology = "PLease provide username"
            return render_template("requirements.html", apology=apology)

        # Ensure password was submitted
        elif not request.form.get("password"):
            apology = "PLease create password"
            return render_template("requirements.html", apology=apology)

        name = request.form.get("username")

        check = db.execute("SELECT * FROM users WHERE username = ?", name)
        if len(check) != 0:
            apology = "This username is already taken"
            return render_template("requirements.html", apology=apology)

        if request.form.get("password") != request.form.get("confirmation"):
            apology = "Passwords don't match"
            return render_template("requirements.html", apology=apology)

        password = request.form.get("password")

        hash_password = generate_password_hash(password)
        db.execute("INSERT INTO users (username, hash, status) VALUES (?, ?, ?)",
                   name, hash_password, "user")

        user_session = db.execute("SELECT id, status FROM users WHERE username = ?",
                                  request.form.get("username"))
        session["user_id"] = user_session[0]["id"]
        session["status"] = user_session[0]["status"]

        # Redirect user to home page
        return redirect("/")
        # else:
        # return apology("password is not strong! min 10 symbols, 1 digit, 1 letter!", 403)

    else:
        return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return render_template("requirements.html", apology="Please provide username")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return render_template("requirements.html", apology="Please enter your password")

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return render_template("requirements.html", apology="Invalid password or username")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        session["status"] = rows[0]["status"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


def login_required(f):
    "Require user to log in for some functions"
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function


def admin_required(f):
    "Require admin status for some actions"
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("status") != "admin":
            return render_template("requirements.html", apology="You need admin status for this operation")
        return f(*args, **kwargs)

    return decorated_function


@app.route("/add_post", methods=["GET", "POST"])
@login_required
@admin_required
def add_post():
    "Add new post to the blog"

    if request.method == "POST":
        if not request.form.get("title"):
            return render_template("requirements.html", apology="Please enter title")
        elif not request.form.get("content"):
            return render_template("requirements.html", apology="Please enter your content")
        elif not "cover" in request.files:
            return render_template("requirements.html", apology="Please choose your cover")

        if 'cover' in request.files:
            file = request.files["cover"]
            file_extension = os.path.splitext(file.filename)[1]
            filename = str(uuid.uuid4()) + file_extension
            app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static', 'uploads')
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            path = url_for('static', filename='uploads/' + filename)
        content = request.form.get("content")
        print(content)
        db.execute("INSERT INTO posts (user_id, title, content, image_path) VALUES (?, ?, ?, ?)",
                   session["user_id"], request.form.get("title"), content, path)
        return redirect("/blog")
    else:
        return render_template("add_post.html")


def select_post(post_id):
    post = db.execute("SELECT * FROM posts WHERE id = ?", post_id)
    if post is None:
        abort(404)
    return post


@app.route("/<int:post_id>")
def show_post(post_id):
    post = select_post(post_id)
    saved = None
    if "user_id" in session:
        saved = db.execute("SELECT * FROM saved_posts WHERE post_id = ? AND user_id = ?",
                        post_id, session["user_id"])
    other_posts = db.execute(
        "SELECT title, image_path, id FROM posts ORDER BY created DESC LIMIT 3")
    return render_template("post.html", post=post, saved=saved, other_posts=other_posts)


@app.route("/savepost", methods=["POST"])
@login_required
def save_post():
    data = request.get_json()
    post_id = data["id"]
    user_id = session["user_id"]
    try:
        db.execute("INSERT INTO saved_posts (user_id, post_id) VALUES (?, ?)", user_id, post_id)
        return jsonify(success=True, message="Post saved!")
    except:
        return jsonify(success=False, message="Sorry, something went wrong, please try again later")


@app.route("/deletepost", methods=["POST"])
@login_required
def delete_saved_post():
    data = request.get_json()
    post_id = data["id"]
    user_id = session["user_id"]
    try:
        db.execute("DELETE FROM saved_posts WHERE user_id = ? AND post_id = ?", user_id, post_id)
        return jsonify(success=True, message="Post removed from saved list")
    except:
        return jsonify(success=False, message="Sorry, something went wrong, please try again later")


@app.route("/blog")
def blog():
    "Displays all the blog posts"
    posts = db.execute("SELECT * FROM posts ORDER BY created DESC")
    return render_template("blog.html", posts=posts)


@app.route("/add_recipe", methods=["GET", "POST"])
@login_required
@admin_required
def add_recipe():
    "Add new post to the blog"

    if request.method == "POST":
        if not request.form.get("title"):
            return render_template("requirements.html", apology="Please enter title")
        elif not request.form.get("content"):
            return render_template("requirements.html", apology="Please enter your content")
        elif not "cover" in request.files:
            return render_template("requirements.html", apology="Please choose your cover")

        if 'cover' in request.files:
            file = request.files["cover"]
            file_extension = os.path.splitext(file.filename)[1]
            filename = str(uuid.uuid4()) + file_extension
            app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static', 'uploads')
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            path = url_for('static', filename='uploads/' + filename)
        content = request.form.get("content")
        print(content)
        db.execute("INSERT INTO recipes (user_id, title, content, image_path) VALUES (?, ?, ?, ?)",
                   session["user_id"], request.form.get("title"), content, path)
        return redirect("/recipes")
    else:
        return render_template("add_recipe.html")


def select_recipe(recipe_id):
    recipe = db.execute("SELECT * FROM recipes WHERE id = ?", recipe_id)
    if recipe is None:
        abort(404)
    return recipe


@app.route("/recipe<int:recipe_id>")
def show_recipe(recipe_id):
    recipe = select_recipe(recipe_id)
    saved = None

    if "user_id" in session:
        saved = db.execute(
            "SELECT * FROM saved_recipes WHERE recipe_id = ? AND user_id = ?", recipe_id, session["user_id"])

    other_recipes = db.execute(
        "SELECT title, image_path, id FROM recipes ORDER BY created DESC LIMIT 3")
    return render_template("recipe.html", recipe=recipe, saved=saved, other_recipes=other_recipes)


@app.route("/saverecipe", methods=["POST"])
@login_required
def save_recipe():
    data = request.get_json()
    recipe_id = data["id"]
    user_id = session["user_id"]
    try:
        db.execute("INSERT INTO saved_recipes (user_id, recipe_id) VALUES (?, ?)", user_id, recipe_id)
        return jsonify(success=True, message="Post saved!")
    except:
        return jsonify(success=False, message="Sorry, something went wrong, please try again later")


@app.route("/deleterecipe", methods=["POST"])
@login_required
def delete_saved_recipe():
    data = request.get_json()
    recipe_id = data["id"]
    user_id = session["user_id"]
    try:
        db.execute("DELETE FROM saved_recipes WHERE user_id = ? AND recipe_id = ?", user_id, recipe_id)
        return jsonify(success=True, message="Post removed from saved list")
    except:
        return jsonify(success=False, message="Sorry, something went wrong, please try again later")


@app.route("/recipes")
def recipes():
    """Displays all the blog posts"""
    recipes = db.execute("SELECT * FROM recipes ORDER BY created DESC")
    return render_template("recipes.html", recipes=recipes)


@app.route("/profile")
@login_required
def profile():
    """Show user profile with all saved posts and recipes"""
    profile = db.execute("SELECT username FROM users WHERE id = ?", session["user_id"])
    saved_posts = db.execute(
        "SELECT title, image_path, posts.id FROM saved_posts JOIN posts ON saved_posts.post_id = posts.id WHERE saved_posts.user_id = ?", session["user_id"])
    saved_recipes = db.execute(
        "SELECT title, image_path, recipes.id FROM saved_recipes JOIN recipes ON saved_recipes.recipe_id = recipes.id WHERE saved_recipes.user_id = ?", session["user_id"])
    return render_template("profile.html", profile=profile, saved_posts=saved_posts, saved_recipes=saved_recipes)
