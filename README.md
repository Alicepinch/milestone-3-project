# Eating Vegan

[Eating Vegan Live Site](https://eating-vegan.herokuapp.com/)

Eating Vegan is an online community where users can create and explore new exclusively vegan recipes with each other. Users of "Eating Vegan" will have the option to create an account where they will be able to login to create, read, update and delete Vegan recipes. 

## Table of Index: 
- [UX](#ux)
   - [User Stories](#user-stories)
   - [Wireframes](#wireframes)
   - [Design](#design)
- [Features](#features)
- [Future Features](#future-features)
- [Technologies Used](#technologies-used)
- [Data Schema](#data-schema)
- [Testing](TESTING.md)
- [Deployment](#deployment)
   - [Github cloning](#creating-a-local-repository)
   - [Heroku deployment](#heroku-deployment)
- [Credits](#credits)
 
## UX

The UX goal of this website is to build a fun, easy to use website for users to view Vegan recipes all in one place. The target audience for this website is anyone who is vegan/vegetarian/exploring veganism who wants to discover or share new recipes with others. All users should be able to view the recipes that have been shared on the website, however if a user creates an account then they will be have added features where they can share and edit their own recipes to the website. Therefore, another goal for this website was to insure the interface was easy to use for users who create an account to create, update,read and delete recipes and their account. 

## User Stories

<details><summary>New User</summary>
<p>

- As a user I would like to be able to login to my account.
- As a user I would like to be able to log out of my account.
- As a user I would like to be able to view my profile.
- As a user I would like to be able to edit or remove recipes that I have created.
- As a user I would like to be able to view all recipes in one place.
- As a user I would like to be able to create new recipes.
- As a user I would like to be able to sign up for the newsletter.
- As a user I would like to be able to update my account details.
- As a user I would like to be able to delete my account.
- As a user I would like to flick through the different meal types.
- As a user I would like to be able to search through all recipes.
- As a user I dont want to have all naviagtion links when not applicable.

</p>

</details>

<details><summary>Returning User</summary>
<p>

- As a new user I would like to be able to register an account.
- As a new user I would like to be able to sign up for the newsletter.
- As a new user I would like to be able to understand what the website is.
- As a new user 

</details>

<details><summary>Admin</summary>
<p>

- As an admin I would like to be able to edit any recipe.
- As an admin I would like the option to delete any recipes incase they don't meet the guidelines.
- As an admin I would like to be able to delete users if needed. 
</p>

</details>

## Wireframes

Wireframes for Eating Vegan were created using balsamiq and can be found below.
As the interface will look different for customers who have registered an account and users who are just visiting there are two wireframes of how this will look.

[User Logged In Wireframes](docs/eating-vegan-wireframe-logged-in.png)

[User Logged Out Wireframes](docs/eating-vegan-wireframe-logged-out.png)

## Design 

Veganism can sometimes be associated with being boring. Therefore, for the overall design of this project I wanted it to be modern but with a fun feel throughout for the user.

<details><summary>Typography</summary>
<p>

Font's I have chosen for this project are 'Bungee Shade', 'Bungee' and 'Roboto'. The reason I have chosen these fonts is because I wanted the design of 'Eating Vegan' to be eye catching and I found the Bungee font's stood out from any others. Bungee Shade will be used for all page headings. Bungee for all subheadings and Roboto will be used for all links, p elements and buttons.

#### Colour Scheme

The main colour's chosen for the website are black and white. As users are able to upload their own photos for the recipes I wanted to insure there wouldn't be any major contrasts in colours therefore opted for black and white. For links and the hover colour for the Navigation bar I chose a green colour. This was due to wanting to include the colour that is mostly associted with veganism but not overusing it on the website. For links and buttons throughout a grey colour has been used as this complimented the black and white well. Lastly, for flash messages on the login, register and update user pages a red colour has been used so that the messages stand out to the customer. Below is the colour palette used:

![Colour Palette](/docs/eating-vegan-colour-palette.jpg)

</p>
</details>

<details><summary>Colour Scheme</summary>
<p>

The main colour's chosen for the website are black and white. As users are able to upload their own photos for the recipes I wanted to insure there wouldn't be any major contrasts in colours therefore opted for black and white. For links and the hover colour for the Navigation bar I chose a green colour. This was due to wanting to include the colour that is mostly associted with veganism but not overusing it on the website. For links and buttons throughout a grey colour has been used as this complimented the black and white well. Lastly, for flash messages on the login, register and update user pages a red colour has been used so that the messages stand out to the customer. Below is the colour palette used:

![Colour Palette](/docs/eating-vegan-colour-palette.jpg)

</p>
</details>

## Data Schema:

### MongoDB

- The database used for this project is an NoSQL database. The database was created using the MongoDB cross-platform document-oriented program.

### Data types

The datatypes that have been used in this project are:
- ObjectId
- String
    
### Collections in database:

For this project I created a database in MongoDB called vegan_cookbook. Inside of this database I created 4 different collections to be used.

#### Users

| Title | Key in db | form validation type | Data type |
--- | --- | --- | --- 
ID | _id | None | ObjectId 
Name | username | text, `maxlength="15"` | string
Email Address | email | email, `maxlength="30"` | string
Password | password | text, `maxlength="15"` | string
Profile Picture | profile_img | url | string
Date joined | date_joined | Populated from when user is created | string

#### Recipes

| Title | Key in db | form validation type | Data type |
--- | --- | --- | --- 
ID | _id | None | ObjectId 
Recipe Name | recipe_name | text | string
Meal Type | meal_type | text | string
Recipe Image | img_url | url | string
Yield | yield | number | string
Active Time | active_time | text | string
Total Time | total_time | textarea | string
Description | description | textare | string
Ingredients | ingredients | textarea | string
Method | method | textarea | string
Recommendations | recomendations | text | string
Created By | created_by | Populated from session['user'] | string
Date Created | date_created | Populated from when form is submitted | string

#### Meals 

| Title | Key in db | form validation type | Data type |
--- | --- | --- | --- 
ID | _id | None | ObjectId 
Meal | meal_type | text | string

#### Subscribers

| Title | Key in db | form validation type | Data type |
--- | --- | --- | --- 
ID | _id | None | ObjectId 
Subscribers | subscriber_email | email `maxlength="30"`| string

## Features

Please note that admin features are only available if the admin is logged in. 
 
- [x] Login
- [x] Register
- [x] Profile Page
- [x] Recipe Page
- [x] Edit Recipe
- [x] Add new recipe
- [x] Newsletter Subscription
- [x] Flash messages
- [x] Search recipes
- [x] If a user is logged out and tries to access any 'login_required' pages they will be redirected to login page.
- [x] Single recipe page.
- [x] 404 page.
- [x] 505 page.
- [x] Update user information.
- [x] Delete account.
- [x] Update password accound.
- [ ] Filter drop down to flick through meal types.
- [x] Admin can manage all recipes 
- [x] Delete modals to prompt users to confirm deletion of account and recipes.

## Future Features

- [ ] Show more button for recipes(pagination)
- [ ] User profiles with option to upload images.
- [ ] Automated email when user signs up.
- [ ] User could upload an image directly to the website.
- [ ] Option to view other users and what they have uploaded.
- [ ] More specific filters for recipes.
- [ ] User can update their username
 
## Technologies Used

- JQuery
    - The project uses **JQuery** to simplify DOM manipulation.
- Python 3.8.2
- Flask
    * Jinja 
    * Werkzeug security
- MongoDB
- HTML
- CSS
- Heroku
- Bootstrap
- Git & GitHub.com

### Other Tools Used

- [Font Awesome](https://fontawesome.com/) 
- [Google fonts](https://fonts.google.com/) 
- [Balsamiq](https://balsamiq.com/) 
- [Gimp](https://www.gimp.org/) 
- [W3Schools](https://www.w3schools.com/) 
- [StackOverflow](https://stackoverflow.com/) 
- [Coloors](https://coolors.co/) 
- [Favicon generator](https://www.favicon-generator.org/) 
- [JShint](https://jshint.com/) 
- [W3cValidator](https://validator.w3.org/)
- Google chrome developer tools.
- [Flask Documentation](https://flask.palletsprojects.com/en/1.1.x/)
  - [Flask error pages](https://flask.palletsprojects.com/en/1.1.x/patterns/errorpages)
  - [For view decorators](https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/)
  - [For permanent session cookie](https://flask.palletsprojects.com/en/1.1.x/config/)

## Testing

All the testing carried out for Eating Vegan can be found [here](TESTING.md)

## Deployment

### Creating a local repository:

In order to run this on your local IDE you need to insure you have the following installed on your machine:

- PIP
- Python
- Git
- You will also need an account on MongoDB 

In order to deploy your own version of this website you will need to clone a local copy of the repository. To do this you need to follow the following steps.

- Click on the 'Code' button next to 'Add a file' when you have opened a repository
- To clone your repository by https:// click on the clipboard icon next to the URL.
- Once you have done this, open the terminal of your own IDE
  - The current directory will need to be changed to where you want your cloned directory.
- Type ```git clone https://github.com/Alicepinch/everything-vegan.git``` into your terminal.

(There are other ways that you can clone a repository and these can be found on the [GitHub docs.](https://docs.github.com/en/github/creating-cloning-and-archiving-repositories))

Once the repository is cloned you will need to ensure that all the packages needed to run this app are installed. To install all packages from requirements.txt file using the following command in terminal.
``` pip3 -r requirements.txt ```

In your local IDE create a file called env.py.
Inside the env.py file create the following environment variables: 

``` 
import os

os.environ.setdefault("IP", "0.0.0.0")
os.environ.setdefault("PORT", "5000")
os.environ.setdefault("SECRET_KEY", `<your_secret_key>`)
os.environ.setdefault("MONGO_URI", "mongodb+srv://<username>:<password>@<cluster_name>-qtxun.mongodb.net/<database_name>?retryWrites=true&w=majority")
os.environ.setdefault("MONGO_DBNAME", `<your_database_name>`)
```

**As some of this information is sensitive, be sure to create a ".gitignore" file and add "env.py"**

### Create a database in MongoDB: 

- Signup or login to your MongoDB account.
- Go to 'Database User' and create a new database user. 
 - This is the username and password that you will include in your 'MONGO_URI' url in the env.py file.
- Create a cluster 
- Once created, click on 'collections' and create a new database.
 - This is the database name that you will need to include in your 'MONGO_DBNAME' in the env.py file.
- Create four collections within your database: meal, recipes, subscribers, users.

### Heroku deployment:

This repository can now be deployed to Heroku:

To deploy this project to Heroku you will need a Heroku acccount.
Once you have an account please follow the below steps. 

1. In Heroku create a new app and set the region to EU. 

2. In your github project create a requirements.txt file using the terminal command ```pip3 freeze —-local > requirements.txt ``` (This is so Heroku can read all of the web apps that have been used in the project)

4. Create a Procfile by typing ```echo web: python app.py > Procfile``` into the terminal.

5. Add all files to github by typing 'git add .' into the terminal to stage all of your files. Then ```git commit -m "<message here>``` to commit the changes ready to be pushed to GitHub.

6. When all your files are ready to be pushed to github, type ```git push``` in the terminal.

5. Back on your Heroku dashboard for your application, go to 'Deploy'.

6. Within this section, scroll down to 'Deployment method' and select 'Connect to GitHub'

7. In the 'Connect to GitHub' section below - search for the github repository name. When you see the repository name click on the 'Connect' button.

8. Confirm the linking of the heroku app to the correct GitHub repository.

9. In the heroku dashboard for the application, click on "Settings" > "Reveal Config Vars".

10. In the fields fill out the following:

| Key | Value |
 --- | ---
DEBUG | FALSE
IP | 0.0.0.0
MONGO_URI | `mongodb+srv://<username>:<password>@<cluster_name>-qtxun.mongodb.net/<database_name>?retryWrites=true&w=majority`
PORT | 5000
SECRET_KEY | `<your_secret_key>`

## Credits

### Content

- Some recipes created by user "alicepinch" and Images have been taken from [BBC goodfood.](https://www.bbcgoodfood.com/)
- Some recipes will have been added by other users. 

### Media

The photos used in this site were from:

- [Background photo used across site](https://www.pexels.com/photo/photo-of-vegetable-salad-in-bowls-1640770/)
- [Default recipe image](https://www.pexels.com/photo/white-and-black-wooden-blocks-3669638/)
- [Default profile Picture](https://www.pexels.com/photo/scrabble-tiles-in-blue-ceramic-plate-2377164/)
- Some recipe images were taken from:
https://www.pexels.com/
https://unsplash.com/ 
