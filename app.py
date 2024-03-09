# FOR RUNNING THE APPLICATION IN BROWSER:
# Open requirements.txt file in VS Code
# In the bottom right corner, you will see 'Create Environment' click on it
# After completion, you will be able to see .venv file in your directory
# Now run the python file, you will get a link to the server in the terminal
# Ctrl + Click to open this in browser
# Everytime you make changes, make sure to refresh the page in browser

from flask import Flask, render_template, redirect, request
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3

# Configure application
app = Flask(__name__)

# Setting up the connection with database
connection = sqlite3.connect("mind-map.db")

# Creating a cursor to execute SQL commands
cursor = connection.cursor()


# Set the default route
@app.route("/")
def index():
  return render_template("welcome.html")

# Login
@app.route("/login", methods=["GET", "POST"])
def login():
  if request.method == "GET":
    return render_template("login.html")
  else:
    return f"Kaam pura hua nhi abhi tak"

# Sign Up
@app.route("/signup", methods=["GET", "POST"])
def signup():
  # Checking whether user clicked on a link or submitted sign up form
  if request.method == "GET":
    return render_template("signup.html")
  else:
    # Extract username, email, password from the form
    username = request.form.get("username")
    email = request.form.get("email")
    password = request.form.get("password")

    # Hash the password
    hashP = generate_password_hash(password)

    # Adding data to 'users' table in database
    cursor.execute("INSERT INTO users (username, email, hashed_password) VALUES (?, ?, ?);", username, email, hashP)

    # Close the cursor and connection as one operation is complete
    cursor.close()
    connection.close()


# Run the application
if __name__ == '__main__':
  app.run(debug=True)