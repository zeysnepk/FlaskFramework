from flask import Flask, render_template # Import the Flask class from the flask module and render_template function


app = Flask(__name__) # Create a new Flask instance
@app.route("/") # Define a route for the homepage URL
def homepage(): # Define the function that will be executed when the homepage URL is accessed
    article = dict()
    article["title"] = "TEST"
    article["body"] = "Zeynep"
    return render_template("index.html", article = article) # Render the index.html template with the provided article dictionary

@app.route("/about") # Define a route for the /about URL
def about(): 
    return "About Page" 

@app.route("/about/zeynep") # Define a route for the /about/zeynep URL
def me():
    return "I'm Zeynep"
    
if __name__ == "__main__": # Check if the script is being run directly
    app.run(debug=True) # Run the Flask application with debug mode enabled
    