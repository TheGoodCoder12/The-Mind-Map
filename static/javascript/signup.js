function validate() {
  var username = document.getElementById('username').value;
  var email = document.getElementById('email').value;
  var password = document.getElementById('password').value;
  var confirmP = document.getElementById('confirmP').value;

  // Checking if password and confirmed password matches
  if (password != confirmP) {
    alert("Password and confirmed password don't match")
    return false;
  }

  // Checking if the password is 8 characters long
  else if (password.length < 8) {
    alert("Password should be atleast 8 characters long")
    return false;
  }

  // Checking if the password has atleast one lowercase, uppercase, digit and special symbol
  var passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[\W_])/;
  if (!passwordRegex.test(password)) {
    alert("Password must contain atleast one lowercase, one uppercase, one digit and one special symbol")
    return false;
  }

  return true;
}


document.addEventListener("DOMContentLoaded", function() {
  var icon = document.getElementById("icon");

        icon.onclick = function () {
            document.body.classList.toggle("dark-theme");

            // Access the image inside the icon div
            var img = icon.querySelector('img');

            // Check if body has light-theme class
            if (document.body.classList.contains("dark-theme")) {
                img.src = "../static/images/light_mode.svg"; // Change the source to light mode image
            } else {
                img.src = "../static/images/dark_light_switch.svg"; // Change the source to dark mode image
            }
        }
});