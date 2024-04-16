# Silk Way Fusion
#### Video Demo:  <https://www.youtube.com/watch?v=sdB2ITbjLsU>
#### Description:
Silk Way Fusion is a food blog with posts and recipes. I love travelling and exploring different cuisines, that's why I've decided to make a platform where I can share my experiences and discoveries.
#### Features
I've made **Flask** webapp using **Python, Django, HTML, CSS and JavaScript**.
I used **Bootstrap** library for some evements of my website like photos carousels, forms control and buttons, and implemented **Trix editor** form for editing new posts.
Also I've made **Sqlite** database to store information about users, posts, recipes and user's saved content.
#### Installation
1. Install Flask, local server and SQLite
2. Clone the repository
3. Navigate to the Project Directory
4. Run Flask application
5. Access the WebApp
#### Usage
You can visit the home page to browse through a collection of recipes and blog posts. Use the navigation menu or just click on a recipe or blog post card to view its details, including the title, description or ingredients and cover image. Enjoy reading through the content and discovering my new recipes from all around the world.

If you'd like to save your favorite recipes or blog posts for easy access later, register for a new account by clicking on the "Register" link in the navigation menu. Once logged in, click on the "Bookmark" button on a recipe or post page to add it to your saved items, which you can view on your profile page.

As an admin user, you have access to additional functionalities for managing the platform such as navigation to the admin panel to add new recipes and blog posts. Use the provided forms to fill out the required fields, including the title, description and upload a cover picture. Use the Trix text editor to create content. After adding all the necessary information, submit the form to publish your recipe or blog post to the platform.

Admin functionality is currently restricted to the project creator. Users cannot register for admin privileges at this time. If you have any questions, inquiries or would like to suggest content for addition, feel free to reach me out via email or social nets provided in the footer.

#### Project Structure
1. Main directory
- app.py \
    This Flask application serves as the backend for a web platform Silk Way Fusion. \
    **Key Features**
    - User Registration and Authentication

    - Flask Users Session Management

    - Database Integration

    - Authorization and Access Control: \
    decorators for login or admin status requirements

    - Dynamic Content Rendering: \
    dynamically rendering HTML templates using Jinja2

    **Routes and Functionality**
    - Home Page (/) \
    Displays a collection of blog posts and recipes.
    Users can navigate to individual post or recipe pages for more details.

    - User Registration (/register) \
    Allows users to register for an account.
    Validates input fields and checks for existing usernames.

    - User Login (/login) \
    Allows registered users to log in to their account.
    Authenticates users with username and password.

    - User Logout (/logout) \
    Logs out the current user and clears the session.

    - Adding New Post (/add_post) \
    Admin users can add new blog posts.
    Validates input fields and uploads a cover image for the post.

    - Saving and Removing Posts (/savepost, /deletepost) \
    Allows users to save or remove blog posts from their saved list.

    - Viewing Blog Posts (/blog) \
    Displays all blog posts with options to view individual posts.

    - Adding New Recipe (/add_recipe) \
    Admin users can add new recipes with similar functionality as adding posts.

    - Saving and Removing Recipes (/saverecipe, /deleterecipe) \
    Allows users to save or remove recipes from their saved list.

    - Viewing Recipes (/recipes) \
    Displays all recipes with options to view individual recipes.

    - User Profile (/profile) \
    Displays user profile with saved blog posts and recipes.

- project.db
    - users table \
    Contains information about the username, user id, hashed password and status of the user.
    - posts table \
    Store blog data such as id, user_id as a foreign key, creation timestamp, title, image_path as a link to the folder with uploaded image and content in HTML format.
    - recipes table \
    Store recipes data such as id, user_id as a foreign key, creation timestamp, title, image_path as a link to the folder with uploaded image and content in HTML format.
    - saved_posts table \
    Information about saved content for each user with user_id and post_id as foreign keys.
    - saved_recipes table \
    Information about saved content for each user with user_id and post_id as foreign keys.

2. Templates folder
- add_post.html: \
    for adding new blog posts by admin user. It includes forms for inputting post content and uploading cover image.

- add_recipe.html: \
    similar to add_post.html, designed for adding new recipes.

- blog.html: \
    this template displays a collection of blog posts.

- index.html: \
    main page of the website with recent posts and general information.

- layout.html: \
    layout template that serves as the base layout for all other pages with header, footer, and common elements shared across multiple pages.

- login.html: \
    user login page.

- post.html: \
    displays an individual blog post with full content.

- profile.html: \
    the user profile page, which displays information about the saved posts and recipes.

- recipe.html: \
    displays an individual recipe with full content.

- recipes.html: \
    this template displays a collection of recipes with links.

- register.html: \
    registration page where new users can sign up for an account.

- requirements.html: \
    requirements for users registration.


3. Static folder
- uploads folder \
    for storing posts and recipes images uploads.
- styles.css \
     contains a series of CSS rules that define the visual styling and layout of the Silk Way Fusion web application.

#### About
This project is the final step of my CS50x course journey, an Introduction to Computer Science from Harvard University.
For more information about the CS50x course and its final project requirements, you can visit the official course website: <https://cs50.harvard.edu/x/2024/project/>

