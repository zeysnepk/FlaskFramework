from flask import Flask, render_template, flash, redirect, url_for, session,logging,request # Import the Flask class from the flask module and render_template function
from flask_mysqldb import MySQL # Import the MySQL class from the flask_mysqldb module 
from wtforms import Form, StringField, TextAreaField, PasswordField, validators 
from passlib.hash import sha256_crypt 


app = Flask(__name__) # Create a new Flask instance

app.config["MYSQL_HOST"] = "localhost" # Define the MySQL host
app.config["MYSQL_USER"] = "root" # Define the MySQL username
app.config["MYSQL_PASSWORD"] = "" # Define the MySQL password
app.config["MYSQL_DB"] = "users_data" # Define the MySQL database name
app.config["MYSQL_CURSORCLASS"] = "DictCursor" # Define the cursor type

mysql = MySQL(app) # Initialize the MySQL class with the Flask application

@app.route("/") # Define a route for the homepage URL
def homepage(): # Define the function that will be executed when the homepage URL is accessed
    return render_template("lay_index.html", answer = "no", op = 1) # Render the layout.html template

@app.route("/about") # Define a route for the /about URL
def about(): 
    number = [1,2,3,4,5]
    
    movies = [
        {"title": "Pulp Fiction", "year": 1994, "director": "Quentin Tarantino"},
        {"title": "The Shawshank Redemption", "year": 1994, "director": "Frank Darabont"},
        {"title": "The Godfather", "year": 1972, "director": "Francis Ford Coppola"},
        {"title": "The Dark Knight", "year": 2008, "director": "Christopher Nolan"},
        {"title": "Eternal Sunshine of the Spotless Mind", "year": 2004, "director": "Michel Gondry"}
    ]
    return render_template("about.html", numbers = number, movies = movies) # Render the about.html template
    

@app.route("/about/zeynep") # Define a route for the /about/zeynep URL
def me():
    article = dict()
    article["title"] = "TEST"
    article["body"] = "Zeynep"
    return render_template("index.html", article = article) # Render the index.html template with the provided article dictionary

@app.route("/movies/<string:id>") # Define a route for the /movies/<id> URL
def detail(id):
    return "Movie Id:" + id # Return the movie ID
    
if __name__ == "__main__": # Check if the script is being run directly
    app.run(debug=True) # Run the Flask application with debug mode enabled
    