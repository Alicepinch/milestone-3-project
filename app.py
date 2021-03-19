import os
from flask import (
    Flask, flash, render_template,
    session, request, url_for, redirect)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from functools import wraps
from datetime import date, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
if os.path.exists("env.py"):
    import env


# Config #

app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=120)

mongo = PyMongo(app)


# Global variables used throughout functions #

default_img = ("/static/images/default-recipe-image.jpg")
default_pic = ("/static/images/default-profile-picture.jpg")
date = date.today()
recipes_data = mongo.db.recipes
users_data = mongo.db.users
subscribers_data = mongo.db.subscribers
meals_data = mongo.db.meals
error = None


def login_required(f):
    """
    Decorator for to be called on views that require users to be logged in.
    """

    @wraps(f)
    def login_check(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return login_check


# Homepage #

@app.route('/')
def index():
    return render_template("index.html")


# Recipe functions #

@app.route('/recipes/<meal>')
def meals(meal):
    """
    When user clicks on different filter options different
    meal types will display.
    """

    if meal == "breakfast":
        recipes = recipes_data.find({"meal_name": "Breakfast"})
    elif meal == "lunch":
        recipes = recipes_data.find({"meal_name": "Lunch"})
    elif meal == "dinner":
        recipes = recipes_data.find({"meal_name": "Dinner"})
    elif meal == "desserts":
        recipes = recipes_data.find({"meal_name": "Desserts"})

    return render_template(
            'recipes.html', meal=meal, recipes=recipes)


@app.route('/recipes')
def recipes():
    """
    Lists all recipes
    in mongodb data.
    """
    recipes = list(recipes_data.find())
    return render_template('recipes.html', recipes=recipes)


@app.route('/recipes', methods=["GET", "POST"])
def search():
    """
    Searches the recipe index. Will return results for, Recipe name,
    description and ingredients. If not results match - flash message
    will show.
    """

    query = request.form.get("search-query")
    all_recipes = recipes_data.find().count()
    recipes = recipes_data.find({"$text": {"$search": query}})

    if all_recipes > 0:
        return render_template("recipes.html", recipes=recipes)

    flash("Sorry! No results found 😔")
    return render_template("recipes.html", recipes=recipes)


@app.route('/recipe/<recipe_id>')
def recipe_page(recipe_id):
    """
    Returns page for
    specific recipe ID.
    """

    recipe = recipes_data.find_one({"_id": ObjectId(recipe_id)})
    return render_template('recipe.html', recipe=recipe)


# Login / register function #

@app.route('/login', methods=["GET", "POST"])
def login():
    """
    Log's customer in if username exists and password is correct.
    """

    if request.method == "GET":
        return render_template("login.html")

    session.permanent = True
    password = request.form.get("password")

    existing_user = users_data.find_one(
        {"username": request.form.get("username").lower()})

    if existing_user and check_password_hash(
                existing_user["password"], password):
        session["user"] = request.form.get("username").lower()

        return redirect(url_for(
                "profile", username=session["user"]))

    flash("Incorrect Username and/or Password")
    return redirect(url_for("login"))


@app.route('/register', methods=["GET", "POST"])
def register():
    """
    Registers new user if username/email is not
    used and add's data to mongo db.
    """

    if request.method == "GET":
        return render_template("register.html")

    existing_username = users_data.find_one(
        {"username": request.form.get("username").lower()})
    existing_email = users_data.find_one(
        {"email": request.form.get("email").lower()})

    if existing_username or existing_email:
        if existing_username:
            flash("Sorry, this username is already in use. Please try another")
        else:
            flash("Sorry, this email is already in use. Please try another")
        return redirect(url_for("register"))

    register = {
        "username": request.form.get("username").lower(),
        "email": request.form.get("email").lower(),
        "password": generate_password_hash(request.form.get("password")),
        "date_joined": date.strftime("%d/%m/%Y"),
        "profile_image": request.form.get(
                                "profile_img") or default_pic,
        "saved_recipes": [],
    }
    users_data.insert_one(register)

    session["user"] = request.form.get("username").lower()
    flash("Welcome! Thank you for sigining up!😊")
    return redirect(url_for(
        "profile", username=session["user"]))


@app.route('/logout')
@login_required
def logout():
    """
    Logs user out from session.
    """

    flash("Goodbye! You have been logged out")
    session.pop("user")
    return redirect(url_for("login"))


# User logged in functions #

@app.route('/profile/<username>', methods=["GET", "POST"])
@login_required
def profile(username):
    """
    Profile will display all recipes created by user.
    If admin is logged in they can view all recipes on profile.
    """

    user = users_data.find_one({"username": session['user']})

    if session['user'] == "admin":
        recipes = list(recipes_data.find())

    recipes = list(recipes_data.find({"created_by": session['user']}))
    return render_template(
        "profile.html", user=user, recipes=recipes, username=username)


@app.route('/add-recipe', methods=["GET", "POST"])
@login_required
def add_recipe():
    """
    Add recipe function allows the
    user to add their own recipes if logged in
    """

    if request.method == "GET":
        return render_template('add-recipe.html')

    recipe = {
        "meal_name": request.form.get("meal_name"),
        "recipe_name": request.form.get("recipe_name"),
        "ingredients": request.form.get("ingredients"),
        "description": request.form.get("description").capitalize(),
        "recommendation": request.form.get("recos").capitalize(),
        "yield": request.form.get("yield"),
        "active_time": request.form.get(
            "active_time").replace('mins', 'minutes').title(),
        "total_time": request.form.get(
            "total_time").replace('mins', 'minutes').title(),
        "img_url": request.form.get("img_url") or default_img,
        "method": request.form.get("method"),
        "created_by": session["user"],
        "date_created": date.strftime("%d/%m/%Y")
    }

    recipes_data.insert_one(recipe)
    flash("Recipe Succesfully Added")
    return redirect(url_for("recipes"))


@app.route('/saved-recipes')
@login_required
def saved_recipes():
    """
    Lists all recipes
    in mongodb data.
    """
    user = users_data.find_one({"username": session["user"]})
    saved = users_data.find_one(user)["saved_recipes"]
    recipe = recipes_data.find_one()

    return render_template('saved-recipes.html', saved=saved, recipe=recipe)


@app.route('/save-recipe/<recipe_id>', methods=["POST"])
@login_required
def save_recipe(recipe_id):
    """
    Adds recipe to a recipe array in users data.
    """
    user = users_data.find_one({"username": session["user"]})
    saved = users_data.find_one(user)["saved_recipes"]
    recipe = recipes_data.find_one({"_id": ObjectId(recipe_id)})

    if request.method == "POST":

        if recipe in saved:
            flash("Recipe already saved!")
            return redirect(url_for("recipes"))
        else:
            users_data.update_one(
                user, {"$push": {"saved_recipes": recipe}})
            flash("Recipe Saved 😊")

    return redirect(url_for("saved_recipes"))


@app.route('/remove-saved-recipe/<recipe_id>', methods=["POST"])
@login_required
def remove_saved_recipe(recipe_id):
    """
    Removes saved recipe from the array in users data.
    """
    username = session["user"]
    user = users_data.find_one({"username": session["user"]})
    recipe = recipes_data.find_one({"_id": ObjectId(recipe_id)})

    flash("Recipe removed from saved")
    users_data.update_one(
                user, {"$pull": {"saved_recipes": recipe}})

    return redirect(url_for("profile", username=username, recipe_id=recipe_id))


@app.route('/edit-recipe/<recipe_id>', methods=["GET", "POST"])
@login_required
def edit_recipe(recipe_id):
    """
    Edit recipe function allows the
    user to edit their own recipes from
    their profile page.
    """

    recipe = recipes_data.find_one({"_id": ObjectId(recipe_id)})

    if request.method == "GET":
        return render_template('edit-recipe.html', recipe=recipe)

    recipes_data.update_one(
        {"_id": ObjectId(recipe_id)},
        {'$set': {
            "meal_name": request.form.get("meal_name"),
            "recipe_name": request.form.get("recipe_name"),
            "ingredients": request.form.get("ingredients"),
            "description": request.form.get("description").capitalize(),
            "recommendation": request.form.get("recos").capitalize(),
            "yield": request.form.get("yield"),
            "active_time": request.form.get(
                "active_time").replace('mins', 'minutes').title(),
            "total_time": request.form.get(
                "total_time").replace('mins', 'minutes').title(),
            "img_url": request.form.get("img_url") or default_img,
            "method": request.form.get("method")
        }})

    flash("Recipe Updated 😊")
    return redirect(url_for("recipe_page", recipe_id=recipe_id))


@app.route('/delete-recipe/<recipe_id>')
@login_required
def delete_recipe(recipe_id):
    """
    Removes recipe from database and recipes page.
    """
    user = users_data.find_one({'username': session['user']})
    created_by = recipes_data.find_one({'created_by': user})

    if created_by:
        recipes_data.delete_one({"_id": ObjectId(recipe_id)})
        flash("Recipe Succesfully Removed!")
    else:
        flash("This is not your recipe to delete!")

    return redirect(url_for("recipes"))


# Update/ delete users #

@app.route('/delete-account/<username>')
@login_required
def delete_user(username):
    """
    If the session user is the username that is logged in or
    the admin then they can delete their account with this URL.
    """

    if session['user'] == username:
        users_data.remove({"username": session['user']})
        session.pop("user")
        recipes_data.remove({"created_by": username})
        flash("Sorry to see you go! Your user has been deleted.")
    else:
        flash("This is not your account to delete!")
        return redirect(url_for("profile", username=username))

    return redirect(url_for("login"))


@app.route('/update-password/<username>', methods=["GET", "POST"])
@login_required
def update_password(username):
    """
    Checks current password is the users password.
    Updates password if the two new passwords match.
    If passwords don't match - flash message appears.
    """

    current_password = request.form.get("password")
    new_password = request.form.get('new-password')
    confirm_password = request.form.get("confirm-password")
    users = users_data
    user = users_data.find_one({'username': session['user']})

    if request.method == "GET":
        return render_template('update-password.html', username=username)

    if check_password_hash(user["password"], current_password):
        if new_password == confirm_password:
            users.update_one(
                {'username': session['user']},
                {'$set': {
                    'password': generate_password_hash
                    (new_password)
                }})
            flash("Password updated! 😊")
            return redirect(url_for('profile', username=username))

        flash("Passwords do not match! Please try again😔")
        return redirect(url_for("update_password", username=username))

    flash('Incorrect password. Please try again😔')
    return redirect(url_for('update_password', username=username))


@app.route('/update-profile-pic/<username>', methods=["GET", "POST"])
@login_required
def update_profile_pic(username):
    """
    Updates users profile photo.
    """

    if session['user'] == username:
        users_data.update_one(
            {"username": session['user']},
            {'$set': {
                "profile_image": request.form.get(
                                    "profile_img")
                }})

    return redirect(url_for("profile", username=username))


# Newsletter Subscribe #

@app.route('/subscribe', methods=["GET", "POST"])
def subscribe_user():
    """
    First checks if email is subscribed already.
    If email is not subscribed, email is added to database.
    """

    existing_sub = subscribers_data.find_one(
            {"subscriber_email": request.form.get("sub_email")})
    if existing_sub:
        return redirect(request.referrer + "#message")
    subscribe = {
        "subscriber_email": request.form.get("sub_email"),
        }
    subscribers_data.insert_one(subscribe)
    return redirect(request.referrer + "#message")


# Error Pages #

@app.errorhandler(404)
def page_not_found(error):
    return render_template('/errors/404.html'), 404


@app.errorhandler(500)
def internal_server_error(error):
    return render_template('/errors/500.html'), 500


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
