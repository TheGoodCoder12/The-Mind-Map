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