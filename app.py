# FOR RUNNING THE APPLICATION IN BROWSER:
# Open requirements.txt file in VS Code
# In the bottom right corner, you will see 'Create Environment' click on it
# After completion, you will be able to see .venv file in your directory
# Now run the python file, you will get a link to the server in the terminal
# Ctrl + Click to open this in browser
# Everytime you make changes, make sure to refresh the page in browser

# Importing required libraries and functions
from flask import Flask, render_template, redirect, request, g, session
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3
from extra import isStrong, login_required

# Configure application
app = Flask(__name__)
app.secret_key = 'nothing here'

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
      return f"Please enter all required fields to proceed"
    
    # Hashing the obtained password
    hashEnterP = generate_password_hash(enterPassword)

    # Obtain database connection
    connection = get_db()

    # Creating a cursor to execute SQL commands
    cursor = connection.cursor()

    # Getting user's password from database and checking email id
    cursor.execute("SELECT hashed_password FROM users where email = ?;", [email])
    userPassword = cursor.fetchone()
    if not userPassword:  # no password found for entered email id
      cursor.close()
      return f"Please enter a valid registered email id"
    
    # Checking password entered by the user
    if not check_password_hash(userPassword[0], enterPassword):
      cursor.close()
      return f"Incorrect password"
    else:
      # Entered email and password is correct, redirect the user to home page after setting up the session
      userData = cursor.execute("SELECT id, username FROM users where email = ?;", [email])
      for USERid, USERname in userData:
        session['user_id'] = USERid
        session['username'] = USERname
      session['email'] = email

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
    confirmP = request.form.get("confirmP")

    # Checking if any field is empty - check1
    if not username or not email or not password or not confirmP:
      return f"Please enter all required fields"
    # Checking if password and confirmed password match - check2
    elif confirmP != password:
      return f"New password and confirmed password don't match"
    # Checking if password is atleast 8 characters long - check3
    elif len(password) < 8:
      return f"Password should be atleast 8 characters long"
    
    # Checking if password is strong enough - check4
    if not isStrong(password):
      return f"Password should contain atleast one uppercase, one lowercase, one digit and one special character"

    # Obtain database connection
    connection = get_db()

    # Creating a cursor to execute SQL commands
    cursor = connection.cursor()

    # Checking if email or username of user already exists - check5
    data = cursor.execute("SELECT email, username FROM users;")
    for EMAIL, USERNAME in data:
      if EMAIL == email:
        return f"Email id already exists"
      elif USERNAME == username:
        return f"Username already exists, please choose another"

    # Hash the password
    hashP = generate_password_hash(password)

    # Adding data to 'users' table in database
    cursor.execute("INSERT INTO users (username, email, hashed_password) VALUES (?, ?, ?);", [username, email, hashP])

    # Making a commit so that changes get saved in the database
    connection.commit()

    # Close the cursor as operation is complete
    cursor.close()

    # Redirect the user to homepage
    print(f"entered email is {email}, entered password is {password}, hashP = {hashP}")
    return redirect("/login")


# Home page
@app.route("/home")
@login_required
def home():
  return render_template("index.html")


# Clue Organization
@app.route("/clue", methods=["GET", "POST"])
@login_required
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
@login_required
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


@app.route("/profile")
@login_required
def profile():
  if request.method == 'GET':
    return render_template("profile.html", username=session['username'], email=session['email'])


# Log out
@app.route("/logout")
@login_required
def logout():
  session.clear()
  return redirect("/")
  

# Run the application+
if __name__ == '__main__':
  app.run(debug=True)