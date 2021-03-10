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
default_reco = "No Recommendations for this recipe"
default_pic = ("/static/images/default-profile-picture.jpg")
date = date.today()
recipes_data = mongo.db.recipes
users_data = mongo.db.users
subscribers_data = mongo.db.subscribers
meals_data = mongo.db.meals


def login_required(f):
    @wraps(f)
    def login_check(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('login'))
        else:
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
    Filters different meal types from data.
    """
    if meal == "breakfast":
        recipes = list(
            recipes_data.find({
                "$query": {
                    "meal_name": "Breakfast"
                    }
            })
        )
    elif meal == "lunch":
        recipes = list(
            recipes_data.find({
                "$query": {
                    "meal_name": "Lunch"
                    }
            })
        )
    elif meal == "dinner":
        recipes = list(
            recipes_data.find({
                "$query": {
                    "meal_name": "Dinner"
                    }
            })
        )
    elif meal == "desserts":
        recipes = list(
            recipes_data.find({
                "$query": {
                    "meal_name": "Desserts"
                    }
            })
        )

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


@app.route('/search', methods=["GET", "POST"])
def search():
    """
    Searches the recipe index.
    Will return results for, Recipe name,
    description and ingredients.
    If not results match - flash message
    will show.
    """
    query = request.form.get("search-query")
    all_recipes = recipes_data.find().count()
    recipes = recipes_data.find({"$text": {"$search": query}})

    if all_recipes > 0:
        return render_template("recipes.html", recipes=recipes)
    else:
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
    Log's customer in if username
    exists and password is correct.
    """
    session.permanent = True
    password = request.form.get("password")

    if request.method == "POST":

        existing_user = users_data.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            if check_password_hash(
                    existing_user["password"], password):
                session["user"] = request.form.get("username").lower()

                return redirect(url_for(
                    "profile", username=session["user"]))

            else:
                flash("Incorret Username and/or Password")
                return redirect(url_for("login"))

        else:
            flash("Incorrect Username and/or Password")
            return redirect(url_for("login"))

    return render_template("login.html")


@app.route('/register', methods=["GET", "POST"])
def register():
    """
    Registers new user if
    username/email is not used
    and add's data to mongo db.
    """
    if request.method == "POST":

        existing_username = users_data.find_one(
            {"username": request.form.get("username").lower()})
        if existing_username:
            flash("Sorry, this username already exists. Please try another")
            return redirect(url_for("register"))

        existing_email = users_data.find_one(
            {"email": request.form.get("email").lower()})
        if existing_email:
            flash("Sorry, this email is in use. Please try another")
            return redirect(url_for("register"))

        register = {
            "username": request.form.get("username").lower(),
            "email": request.form.get("email").lower(),
            "password": generate_password_hash(request.form.get("password")),
            "date_joined": date.strftime("%d/%m/%Y"),
            "profile_image": request.form.get(
                                 "profile_img") or default_pic
        }
        users_data.insert_one(register)

        session["user"] = request.form.get("username").lower()
        flash("Welcome! Thank you for sigining up!😊")
        return redirect(url_for(
            "profile", username=session["user"]))

    return render_template("register.html")


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
    If the user has added recipes then
    they will display on profile page.
    """
    user = users_data.find_one({"username": session['user']})

    if session['user'] == "admin":
        recipes = list(recipes_data.find())
    else:
        recipes = list(recipes_data.find(
                {"created_by": session['user']}))
    return render_template(
        "profile.html", user=user, recipes=recipes, username=username)


@app.route('/add-recipe', methods=["GET", "POST"])
@login_required
def add_recipe():
    """
    Add recipe function allows the
    user to add their own recipes if logged in
    """
    if request.method == "POST":
        recipe = {
            "meal_name": request.form.get("meal_name"),
            "recipe_name": request.form.get("recipe_name"),
            "ingredients": request.form.get("ingredients"),
            "description": request.form.get("description"),
            "recommendation": request.form.get("recos") or default_reco,
            "yield": request.form.get("yield"),
            "active_time": request.form.get("active_time"),
            "total_time": request.form.get("total_time"),
            "img_url": request.form.get("img_url") or default_img,
            "method": request.form.get("method"),
            "created_by": session["user"],
            "date_created": date.strftime("%d/%m/%Y")
        }

        recipes_data.insert_one(recipe)
        flash("Recipe Succesfully Added")
        return redirect(url_for("recipes"))

    return render_template('add-recipe.html')


@app.route('/edit-recipe/<recipe_id>', methods=["GET", "POST"])
@login_required
def edit_recipe(recipe_id):
    """
    Edit recipe function allows the
    user to edit their own recipes from
    their profile page.
    """
    username = users_data.find({'username': session['user']})

    if request.method == "POST":
        recipes_data.update_one(
            {"_id": ObjectId(recipe_id)},
            {'$set': {
                "meal_name": request.form.get("meal_name"),
                "recipe_name": request.form.get("recipe_name"),
                "ingredients": request.form.get("ingredients"),
                "description": request.form.get("description"),
                "recommendation": request.form.get("recos") or default_reco,
                "yield": request.form.get("yield"),
                "active_time": request.form.get("active_time"),
                "total_time": request.form.get("total_time"),
                "img_url": request.form.get("img_url") or default_img,
                "method": request.form.get("method"),
                "created_by": session["user"]
            }})

        flash("Recipe Updated 😊")
        return redirect(url_for("profile", username=username))

    recipe = recipes_data.find_one({"_id": ObjectId(recipe_id)})
    return render_template('edit-recipe.html', recipe=recipe)


@app.route('/delete-recipe/<recipe_id>')
@login_required
def delete_recipe(recipe_id):
    """
    Removes recipe from database and recipes page.
    """
    recipes_data.delete_one({"_id": ObjectId(recipe_id)})
    flash("Recipe Succesfully Removed!")
    return redirect(url_for("recipes"))


# Update/ delete users #


@app.route('/delete-account/<username>')
@login_required
def delete_user(username):
    """
    Ends user session.
    Removes user & all
    recipes created by user.
    """
    users_data.remove({"username": session['user']})
    session.pop("user")
    recipes_data.remove({"created_by": username})

    flash("Sorry to see you go! Your user has been deleted.")
    return redirect(url_for("login"))


@app.route('/update-user/<username>', methods=["GET", "POST"])
@login_required
def update_user(username):
    """
    Checks current password is the users password.
    Updates password if the two new passwords match.
    If passwords dont match - flash message appears.
    """
    current_password = request.form.get("password")
    new_password = request.form.get('new-password')
    confirm_password = request.form.get("confirm-password")
    users = users_data
    user = users_data.find_one({'username': session['user']})

    if request.method == "POST":

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

            else:
                flash("Passwords do not match! Please try again😔")
                return redirect(url_for("update_user", username=username))
        else:
            flash('Incorrect password. Please try again😔')
            return redirect(url_for('update_user', username=username))

    return render_template('update-user.html', username=username)


@app.route('/update-profile-pic/<username>', methods=["GET", "POST"])
@login_required
def update_profile_pic(username):
    """
    Updates users profile photo.
    """
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
        flash("Already Subscribed!")
        return redirect(request.referrer + "#subscribe")

    subscribe = {
        "subscriber_email": request.form.get("sub_email"),
        }
    subscribers_data.insert_one(subscribe)
    flash("Thank you for subscribing!")
    return redirect(request.referrer + "#subscribe")


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
