# FOR RUNNING THE APPLICATION IN BROWSER:
# Open requirements.txt file in VS Code
# In the bottom right corner, you will see 'Create Environment' click on it
# After completion, you will be able to see .venv file in your directory
# Now run the python file, you will get a link to the server in the terminal
# Ctrl + Click to open this in browser
# Everytime you make changes, make sure to refresh the page in browser

# Importing required libraries and functions
from flask import Flask, render_template, redirect, request, g, session, url_for, flash
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3
from utils import isStrong, login_required

# Configure application
app = Flask(__name__)
app.secret_key = 'nothing here'

# Managing the database connection
def get_db():
  db = getattr(g, '_database', None)
  if db is None:
    db= g._database = sqlite3.connect("mind-map.db")
  return db

# Close the connection after each request
def close_db(exception=None):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# Registering teardown function to be called at the end of each request
app.teardown_appcontext(close_db)


# Set the default/root route
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

    # Obtain database connection
    connection = get_db()

    # Creating a cursor to execute SQL commands
    cursor = connection.cursor()

    # Getting user's password from database and checking email id
    cursor.execute("SELECT hashed_password FROM users where email = ?;", [email])
    userPassword = cursor.fetchone()
    if not userPassword:  # no password found for entered email id
      cursor.close()
      flash("Please enter a valid registered email id", 'warning')
      return redirect(url_for("login"))
    
    # Checking password entered by the user
    if not check_password_hash(userPassword[0], enterPassword):
      cursor.close()
      flash("Incorrect password", 'warning')
      return redirect(url_for("login"))
    else:
      # Entered email and password is correct, redirect the user to home page after setting up the session
      userData = cursor.execute("SELECT id, username FROM users where email = ?;", [email])
      for USERid, USERname in userData:
        session['user_id'] = USERid
        session['username'] = USERname
      session['email'] = email

      cursor.close()
      return redirect(url_for("home"))


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

    # Obtain database connection
    connection = get_db()

    # Creating a cursor to execute SQL commands
    cursor = connection.cursor()

    # Checking if email or username of user already exists - check5
    data = cursor.execute("SELECT email, username FROM users;")
    for EMAIL, USERNAME in data:
      if EMAIL == email:
        flash("Email id already exists", 'warning')
        return redirect(url_for("signup"))
      elif USERNAME == username:
        flash("Username already exists, please choose another", 'warning')
        return redirect(url_for("signup"))

    # Hash the password
    hashP = generate_password_hash(password)

    # Adding data to 'users' table in database
    cursor.execute("INSERT INTO users (username, email, hashed_password) VALUES (?, ?, ?);", [username, email, hashP])

    # Making a commit so that changes get saved in the database
    connection.commit()

    # Extracting user id
    cursor.execute("SELECT id FROM users WHERE username = ?;", [username])
    userId = cursor.fetchone()[0]

    # Close the cursor as operation is complete
    cursor.close()

    # Store session data
    session['user_id'] = userId
    session['username'] = username
    session['email'] = email

    # Redirect the user to homepage
    return redirect(url_for("home"))


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
    date = request.form.get("date")
    description = request.form.get("description")

    # Checking if any field is left blank
    if not category or not date or not description:
      flash("Please input all the required details", 'warning')
      return redirect(url_for("clue"))

    # Obtain database connection
    connection = get_db()

    # Creating a cursor to execute SQL commands
    cursor = connection.cursor()

    # Adding data to database
    cursor.execute("INSERT INTO clues (category, date, description, user_id) VALUES (?, ?, ?, ?);", [category, date, description, session['user_id']])

    # Making a commit so that changes get saved in the database
    connection.commit()

    # Close the cursor as operation is complete
    cursor.close()

    # Reload page
    flash("Clue added successfully!", 'success')
    return redirect(url_for("clue"))


# People tracker
@app.route("/people", methods=["GET", "POST"])
@login_required
def people():
  if request.method == "GET":
    return render_template("ppl.html")
  else:
    # Extracting info from the people tracker form
    name = request.form.get("name")
    profession = request.form.get("profession")
    details = request.form.get("details")

    # Checking if any field is left blank
    if not name or not profession or not details:
      flash("Please input all the required details", 'warning')
      return redirect(url_for("people"))

    # Obtain database connection
    connection = get_db()

    # Creating a cursor to execute SQL commands
    cursor = connection.cursor()

    # Adding database to database
    cursor.execute("INSERT INTO people (name, profession, details, user_id) VALUES (?, ?, ?, ?);", [name, profession, details, session['user_id']])

    # Making a commit so that changes get saved in the database
    connection.commit()

    # Close the cursor as operation is complete
    cursor.close()

    # Reload page
    flash("Person added to tracker successfully!", 'success')
    return redirect(url_for("people"))


# Profile
@app.route("/profile")
@login_required
def profile():
  if request.method == 'GET':
    return render_template("profile.html", username=session['username'], email=session['email'])


# Change username
@app.route("/changeUsername", methods=["GET", "POST"])
@login_required
def changeUsername():
  if request.method == "GET":
    return render_template("changeUsername.html")
  else:
    newUsername = request.form.get("newUsername")
    password = request.form.get("password")
    confirmP = request.form.get("confirmP")
    #Checking if any field left blank
    if not newUsername or not password or not confirmP:
      flash("Please input all required fields", 'warning')
      return redirect(url_for("changeUsername"))
    # Checking if both passwords don't match
    elif password != confirmP:
      flash("Password and confirmed password don't match", 'warning')
      return redirect(url_for("changeUsername"))
    
    # Obtain database connection
    connection = get_db()

    # Creating a cursor to execute SQL commands
    cursor = connection.cursor()

    # Getting user password
    cursor.execute("SELECT hashed_password FROM users WHERE id = ?;", [session['user_id']])

    # Checking if entered password is correct
    userPassword = cursor.fetchone()[0]
    if not check_password_hash(userPassword, password):
      flash("Incorrect password", 'warning')
      return redirect(url_for("changeUsername"))
    else:
      # Checking if new username is same as old username
      if newUsername == session['username']:
        flash("New username can't be same as old username", 'warning')
        return redirect(url_for("changeUsername"))
      # Everything is fine, change username
      cursor.execute("UPDATE users SET username = ? WHERE id = ?;", [newUsername, session['user_id']])
      connection.commit()
      cursor.close()

      # Update data in current session
      session['username'] = newUsername

      # Redirect to homepage
      flash("Username changed successfully!", 'success')
      return redirect(url_for("home"))


# Change email
@app.route("/changeEmail", methods=["GET", "POST"])
@login_required
def changeEmail():
  if request.method == "GET":
    return render_template("changeEmail.html")
  else:
    newEmail = request.form.get("newEmail")
    password = request.form.get("password")
    confirmP = request.form.get("confirmP")
    # Checking if any field left blank
    if not newEmail or not password or not confirmP:
      flash("Please input all required fields", 'warning')
      return redirect(url_for("changeEmail"))
    # Checking if both passwords don't match
    elif password != confirmP:
      flash("Password and confirmed password don't match", 'warning')
      return redirect(url_for("changeEmail"))
    # Obtain database connection
    connection = get_db()

    # Creating a cursor to execute SQL commands
    cursor = connection.cursor()

    # Getting user password
    cursor.execute("SELECT hashed_password FROM users WHERE id = ?;", [session['user_id']])

    # Checking if entered password is correct
    userPassword = cursor.fetchone()[0]
    if not check_password_hash(userPassword, password):
      flash("Incorrect password", 'warning')
      return redirect(url_for("changeEmail"))
    else:
      # Checking if new email address is same as old email address
      if newEmail == session['email']:
        flash("New email address can't be same as old email address", 'warning')
        return redirect(url_for("changeEmail"))
      # Everything is fine, change username
      cursor.execute("UPDATE users SET email = ? WHERE id = ?;", [newEmail, session['user_id']])
      connection.commit()
      cursor.close()

      # Update data in current session
      session['email'] = newEmail

      # Redirect to homepage
      flash("Email changed successfully!", 'success')
      return redirect(url_for("home"))


# Change Password
@app.route("/changePassword", methods=["GET", "POST"])
@login_required
def changePassword():
  if request.method == "GET":
    return render_template("changePassword.html")
  else:
    password = request.form.get("currentP")
    newP = request.form.get("newP")
    confirmNewP = request.form.get("confirmNewP")
    #Checking if any field left blank
    if not password or not newP or not confirmNewP:
      flash("Please enter all required fields", 'warning')
      return redirect(url_for("changePassword"))
    # Checking if both passwords match
    elif newP != confirmNewP:
      flash("New password and confirmed new password don't match", 'warning')
      return redirect(url_for("changePassword"))
    # Checking if password is atleast 8 characters long
    elif len(newP) < 8:
      flash("New password should be atleast 8 characters long", 'warning')
      return redirect(url_for("changePassword"))
    # Checking if password is strong enough
    if not isStrong(newP):
      flash("New password should contain atleast one uppercase, one lowercase, one digit and one special character", 'warning')
      return redirect(url_for("changePassword"))
    
    # Obtain database connection
    connection = get_db()

    # Creating a cursor to execute SQL commands
    cursor = connection.cursor()

    # Getting user password
    cursor.execute("SELECT hashed_password FROM users WHERE id = ?;", [session['user_id']])

    # Checking if entered password is correct
    userPassword = cursor.fetchone()[0]
    if not check_password_hash(userPassword, password):
      flash("Incorrect password", 'warning')
      return redirect(url_for("changePassword"))
    else:
      # Checking if new password is same as old password
      if newP == password:
        flash("New password can't be same as old password", 'warning')
        return redirect(url_for("changePassword"))
      # Everything is fine, change password
      hashedNewP = generate_password_hash(newP)
      cursor.execute("UPDATE users SET hashed_password = ? WHERE id = ?;", [hashedNewP, session['user_id']])
      connection.commit()
      cursor.close()

      # Redirect user to homepage
      flash("Password changed successfully!", 'success')
      return redirect(url_for("home"))


# Timeline
@app.route("/timeline")
@login_required
def timeline():
  # Obtain database connection
  connection = get_db()

  # Creating a cursor to execute SQL commands
  cursor = connection.cursor()

  # Set row factory to return dictionaries
  cursor.row_factory = sqlite3.Row

  # Quering the database to get info about clues
  cursor.execute("SELECT * FROM clues WHERE user_id = ? ORDER BY date DESC;", [session['user_id']])
  clueData = cursor.fetchall()

  cursor.close()

  # Render the template with clue data
  return render_template("timeline.html", clueData=clueData)


# Search
@app.route("/search", methods=["GET", "POST"])
@login_required
def search():
  if request.method == "GET":
    return render_template("search.html")
  else:
    date = request.form.get("date")
    people = request.form.get("people")
    clues = request.form.get("clues")

    # Obtain database connection
    connection = get_db()

    # Creating a cursor to execute SQL commands
    cursor = connection.cursor()

    # Set row factory to return dictionaries
    cursor.row_factory = sqlite3.Row

    # Display date related searches
    if date and not people and not clues:
      cursor.execute("SELECT * FROM clues WHERE date = ? AND user_id = ?", [date, session['user_id']])
      cluesByDate = cursor.fetchall()
      cursor.close()
      return render_template("search.html", cluesByDate=cluesByDate)
    # Display people related searches
    elif not date and people and not clues:
      cursor.execute("SELECT * FROM people WHERE name LIKE ? AND user_id = ?;", ['%' + people + '%', session['user_id']])
      peopleData = cursor.fetchall()
      cursor.close()
      return render_template("search.html", peopleData=peopleData)
    # Display clue related searches from their description
    else:
      cursor.execute("SELECT * FROM clues WHERE description LIKE ? AND user_id = ?;", ['%' + clues + '%', session['user_id']])
      cluesInfo = cursor.fetchall()
      cursor.close()
      return render_template("search.html", cluesInfo=cluesInfo)


# Log out
@app.route("/logout")
@login_required
def logout():
  session.clear()
  return redirect(url_for("welcome"))
  

# Run the application+
if __name__ == '__main__':
  app.run(debug=True)