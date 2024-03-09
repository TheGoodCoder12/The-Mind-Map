 // Toggle between login and signup forms
 document.querySelector('a[href="#signup"]').addEventListener('click', function(e) {
    e.preventDefault();
    document.getElementById('signup').style.display = 'block';
    document.querySelector('a[href="#signup"]').style.display = 'none';
    document.querySelector('a[href="#"]').style.display = 'block';
});

document.querySelector('a[href="#"]').addEventListener('click', function(e) {
    e.preventDefault();
    document.getElementById('signup').style.display = 'none';
    document.querySelector('a[href="#signup"]').style.display = 'block';
    document.querySelector('a[href="#"]').style.display = 'none';
});