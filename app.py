# FOR RUNNING THE APPLICATION IN BROWSER:
# Open requirements.txt file in VS Code
# In the bottom right corner, you will see 'Create Environment' click on it
# After completion, you will be able to see .venv file in your directory
# Now run the python file, you will get a link to the server in the terminal
# Ctrl + Click to open this in browser
# Everytime you make changes, make sure to refresh the page in browser

from flask import Flask, render_template, redirect, request

# Configure application
app = Flask(__name__)

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
  if request.method == "GET":
    return render_template("signup.html")
  else:
    return f"Kaam chalu h mommy"

# Run the application
if __name__ == '__main__':
  app.run(debug=True)