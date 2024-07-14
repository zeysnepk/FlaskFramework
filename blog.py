from flask import Flask, render_template, flash, redirect, url_for, session,logging,request # Import the Flask class from the flask module and render_template function
from flask_mysqldb import MySQL # Import the MySQL class from the flask_mysqldb module 
from wtforms import Form, StringField, TextAreaField, PasswordField, validators 
from passlib.hash import sha256_crypt # Import the sha256_crypt module for password hashing
from functools import wraps # Decorator function to ensure the decorated function wraps other functions

def login_required(f): # Decorator function to check if the user is logged in before accessing a route
    @wraps(f)   # Wrap the decorated function in a new function to check if the user is logged in
    def decorated_function(*args, **kwargs): 
        if "logged" in session:  # Check if the user is logged in
            return f(*args, **kwargs) # If the user is logged in, call the decorated function
        else:
            flash("You need to login first", "danger") # Flash an error message if the user is not logged in
            return redirect(url_for("login")) # Redirect to the login page if the user is not logged in
    return decorated_function # Return the decorated function

class Register(Form):
    name = StringField("Name", validators=[validators.Length(min=4, max=25), validators.DataRequired(message="Enter name")]) # Define a name field with validation
    surname = StringField("Surname", validators=[validators.Length(min=4, max=25), validators.DataRequired(message="Enter surname")]) # Define a surname field with validation
    email = StringField("E-mail", validators=[validators.DataRequired(message=("Enter e-mail address")), validators.Email(message="Invalid email")])
    username = StringField("Username", validators=[validators.Length(min=4, max=20), validators.DataRequired(message="Enter username")]) # Define a username field with validation
    password = PasswordField("Password", validators=[validators.DataRequired(message="Enter password"), validators.EqualTo(fieldname="confirm", message="Passwords do not match")]) # Define a password field with validation and a confirm password field with the same name
    confirm = PasswordField("Confirm Password") # Define a confirm password field with the same name
    
class Login(Form): 
    username = StringField("Username")
    password = PasswordField("Password")
    
class MessageForm(Form):
    title = StringField("Message Title", validators = [validators.Length(min=5, max=30)])
    message = TextAreaField("Message", validators = [validators.Length(min=10)])
    
app = Flask(__name__) # Create a new Flask instance

app.secret_key = "zeynep" # Set a secret key for session management

app.config["MYSQL_HOST"] = "127.0.0.1" # Define the MySQL host
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

@app.route("/messages/<string:id>") # Define a route for the /movies/<id> URL
def detail(id):
    return "Movie Id:" + id # Return the movie ID

@app.route("/register", methods = ['GET', 'POST']) # Define a route for the /register URL with GET and POST methods
def register():
    form = Register(request.form) # Create a new instance of the Register form class
    if request.method == "POST" and form.validate(): # Check if the form was submitted
        name = form.name.data # Get the name field value
        surname = form.surname.data
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.encrypt(form.password.data) # Encrypt the password using sha256_crypt
        
        cursor = mysql.connection.cursor() # Create a new cursor
        cursor.execute("INSERT INTO members (name, surname, email, username, password) VALUES(%s, %s, %s, %s, %s)",(name, surname, email, username, password)) # Execute the SQL INSERT query
        mysql.connection.commit() # Commit the transaction
        cursor.close() # Close the cursor
        
        flash("Registration successful!", "success") # Flash a success message with the specified message and category
        return redirect(url_for("login")) # Redirect to the login URL after successful form submission
    else:
        return render_template("register.html", form = form) # Render the register.html template with the provided form

@app.route("/login", methods = ['GET', 'POST'])
def login():
    form = Login(request.form) # Create a new instance of the Login form class
    if request.method == "POST": # Check if the form was submitted
        username = form.username.data 
        password = form.password.data
        
        cursor = mysql.connection.cursor() 
        result = cursor.execute("SELECT * FROM members WHERE username = %s", (username,)) # Execute the SQL SELECT query
        if result > 0: # Check if a user with the provided username exists
            data = cursor.fetchone() # Fetch the user data
            if sha256_crypt.verify(password, data["password"]): # Check if the provided password matches the hashed password
                flash("Login successful!", "success")
                session["logged"] = True # Set a session variable to indicate that the user is logged
                session["username"] = username # Set the session variable to the user's username
                return redirect(url_for("homepage"))
            else:
                flash("Incorrect password", "danger") 
                return redirect(url_for("login"))
        else:
            flash("No user found", "danger") 
            return redirect(url_for("login"))
    return render_template("login.html", form = form) # Render the login.html template
    
@app.route("/logout") # Define a route for the /logout URL
def logout():
    session.clear() # Clear all session variables
    return redirect(url_for("homepage")) # Redirect to the homepage URL


@app.route("/dashboard") # Define a route for the /dashboard URL
@login_required  # Check if the user is logged in before accessing the route
def dashboard():
    cursor = mysql.connection.cursor()
    messages = cursor.execute("SELECT * FROM messages WHERE user = %s", (session["username"],)) 
    if messages > 0:
        messages = cursor.fetchall() 
        return render_template("dashboard.html", messages=messages)  # Render the dashboard.html template with fetched messages  # Render the dashboard.html template with fetched messages  # Render the dashboard.html template with fetched messages  # Render the dashboard.html template with fetched messages  # Render the dashboard.html template with fetched messages  # Render the dashboard.html template with fetched messages  # Render the dashboard.html template with fetched messages  # Render the dashboard.html template with fetched
    else:
        return render_template("dashboard.html") # Render the dashboard.html template

@app.route("/addmessage", methods = ['GET','POST']) 
def add_message(): 
    form = MessageForm(request.form)  # Create a new instance of the MessageForm class  # Fetch user data from session
    if request.method == 'POST' and form.validate(): # Check if form data is valid
        title = form.title.data 
        message = form.message.data
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO messages (title, user, message) VALUES(%s, %s, %s)",(title, session["username"], message))
        mysql.connection.commit()
        cursor.close()
        flash("Message added successfully!", "success")
        return redirect(url_for("dashboard"))
    return render_template("add_message.html", form=form) # Render the add_message.html template with the provided form

    
@app.route("/messages") 
def show_messages():
    cursor = mysql.connection.cursor()
    messages = cursor.execute("SELECT * FROM messages")
    if messages > 0:
        messages = cursor.fetchall()
        return render_template("messages.html", messages=messages) # Render the messages.html template with fetched messages
    else:
        return render_template("messages.html")
    
@app.route("/message/<string:id>") # Define a route for the /message/<id> URL
def message(id):
    cursor = mysql.connection.cursor()
    message = cursor.execute("SELECT * FROM messages WHERE id = %s", (id,))
    if message > 0:
        message = cursor.fetchone()
        return render_template("message.html", message=message) #
    else:
        return render_template("message.html")
    
@app.route("/delete/<string:id>") # Define a route for the /delete/<id> URL
@login_required  # Check if the user is logged in before accessing the route
def delete(id):
    cursor = mysql.connection.cursor()
    message = cursor.execute("SELECT * FROM messages WHERE user = %s AND id = %s",(session["username"], id))
    if message > 0:
        message = cursor.execute("DELETE FROM messages WHERE id = %s", (id,))
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for("dashboard"))
    else:
        flash("No message found", "danger") # Flash a failure message with the specified message and category
        return redirect(url_for("homepage"))

@app.route("/edit/<string:id>", methods = ['GET', 'POST']) 
@login_required
def update(id):
    if request.method == 'GET':
        cursor = mysql.connection.cursor()
        message = cursor.execute("SELECT * FROM messages WHERE user = %s AND id = %s", (session["username"], id))
        if message > 0:
            message = cursor.fetchone()
            form = MessageForm()
            form.title.data = message["title"]
            form.message.data = message["message"]
            return render_template("update.html", form=form)
        else:
            flash("No message found", "danger")
            return redirect(url_for("homepage"))
    else:
        form = MessageForm(request.form)
        new_title = form.title.data # Get the new title field value
        new_message = form.message.data # Get the new message field value
        cursor = mysql.connection.cursor()
        cursor.execute("UPDATE messages SET title=%s, message=%s WHERE id = %s", (new_title, new_message, id)) # Execute the SQL UPDATE query
        mysql.connection.commit()
        cursor.close()
        flash("Message updated successfully!", "success")
        return redirect(url_for("dashboard"))
    
@app.route("/search", methods = ['GET', 'POST']) # Define a route for the /search URL with GET and POST methods
def search():
    if request.method == 'GET':
        return redirect(url_for("homepage"))
    else:
        keyword = request.form.get("keyword") # Get the keyword from the search form
        cursor = mysql.connection.cursor()
        result = cursor.execute("SELECT * FROM messages WHERE title LIKE '%" + keyword + "%' ") # Execute the SQL SELECT query with the keyword search condition
        if result > 0:
            result = cursor.fetchall()
            return render_template("messages.html", messages=result)
        else:
            flash("No messages found", "warning")
            return redirect(url_for("show_messages"))
        
if __name__ == "__main__": # Check if the script is being run directly
    app.run(debug=True) # Run the Flask application with debug mode enabled   