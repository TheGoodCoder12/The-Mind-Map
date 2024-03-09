# FOR RUNNING THE APPLICATION IN BROWSER:
# Open requirements.txt file in VS Code
# In the bottom right corner, you will see 'Create Environment' click on it
# After completion, you will be able to see .venv file in your directory
# Now run the python file, you will get a link to the server in the terminal
# Ctrl + Click to open this in browser
# Everytime you make changes, make sure to refresh the page in browser

# Importing required libraries and functions
from flask import Flask, render_template, redirect, request, g
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3

# Configure application
app = Flask(__name__)

# Managing the database connection
def get_db():
  db = getattr(g, '_database', None)
  if db is None:
    db= g._database = sqlite3.connect("mind-map.db")
  return db


# Set the default route
@app.route("/")
def welcome():
  return render_template("welcome.html")


# Login
@app.route("/login", methods=["GET", "POST"])
def login():
  # Checking whether user clicked on a link or submitted login form
  if request.method == "GET":
    return render_template("login.html")
  else:
    # Extract email, password from the login form
    email = request.form.get("email")
    enterPassword = request.form.get("password")

    # Checking if user left any field blank
    if not email or not enterPassword:
      print("Please enter all required fields to proceed")
      return
    
    # Hashing the obtained password
    hashEnterP = generate_password_hash(enterPassword)

    # Obtain database connection
    connection = get_db()

    # Creating a cursor to execute SQL commands
    cursor = connection.cursor()

    # Getting user's password from database and checking email id
    cursor.execute("SELECT hashed_password FROM users where email = ?;", email)
    userPassword = cursor.fetchone()
    if not userPassword:  # no password found for entered email id
      print("Please enter a valid registered email id")
      cursor.close()
      return
    
    # Checking password entered by the user
    if not check_password_hash(hashEnterP, userPassword):
      print("Incorrect password")
      cursor.close()
      return
    else:
      # Entered email and password is correct, redirect the user to home page
      cursor.close()
      return redirect("/home")


# Sign Up
@app.route("/signup", methods=["GET", "POST"])
def signup():
  # Checking whether user clicked on a link or submitted sign up form
  if request.method == "GET":
    return render_template("signup.html")
  else:
    # Extract username, email, password from the sign up form
    username = request.form.get("username")
    email = request.form.get("email")
    password = request.form.get("password")

    # Hash the password
    hashP = generate_password_hash(password)

    # Obtain database connection
    connection = get_db()

    # Creating a cursor to execute SQL commands
    cursor = connection.cursor()

    # Adding data to 'users' table in database
    cursor.execute("INSERT INTO users (username, email, hashed_password) VALUES (?, ?, ?);", [username, email, hashP])

    # Making a commit so that changes get saved in the database
    connection.commit()

    # Close the cursor as operation is complete
    cursor.close()

    # Redirect the user to homepage
    return redirect("/home")


# Home page
@app.route("/home")
def home():
  return render_template("index.html")


# Clue Organization
@app.route("/clue", methods=["GET", "POST"])
def clue():
  if request.method == "GET":
    return render_template("clue.html")
  else:
    # Extracting info from the clue organization form
    category = request.form.get("category")
    datetime = request.form.get("datetime")
    detail = request.form.get("description")

    # Obtain database connection
    connection = get_db()

    # Creating a cursor to execute SQL commands
    cursor = connection.cursor()

    # Adding data to database
    cursor.execute("INSERT INTO clues (category, datetime, description) VALUES (?, ?, ?);", [category, datetime, detail])

    # Making a commit so that changes get saved in the database
    connection.commit()

    # Close the cursor as operation is complete
    cursor.close()

    # Reload page
    return redirect("/clue")


# People tracker
@app.route("/people")
def people():
  if request.method == "GET":
    return render_template("ppl.html")
  else:
    # Extracting info from the people tracker form
    name = request.form.get("name")
    profession = request.form.get("profession")
    details = request.form.get("details")

    # Obtain database connection
    connection = get_db()

    # Creating a cursor to execute SQL commands
    cursor = connection.cursor()

    # Adding database to database
    cursor.execute("INSERT INTO people (name, profession, details) VALUES ();", [name, profession, details])

    # Making a commit so that changes get saved in the database
    connection.commit()
    
    # Close the cursor as operation is complete
    cursor.close()

    # Reload page
    return redirect("/people")


# Run the application
if __name__ == '__main__':
  app.run(debug=True)