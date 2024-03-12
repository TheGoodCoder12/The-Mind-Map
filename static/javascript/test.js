document.getElementById('searchForm').addEventListener('submit', function(event) {
  event.preventDefault();
  var searchQuery = document.getElementById('searchInput').value;

  fetch('search.php?query=' + encodeURIComponent(searchQuery))
    .then(response => response.json())
    .then(data => {
      var searchResults = document.getElementById('searchResults');
      searchResults.innerHTML = ''; // Clear previous search results

      if (data.length === 0) {
        searchResults.innerHTML = 'No results found.';
      } else {
        data.forEach(result => {
          var resultItem = document.createElement('div');
          resultItem.textContent = result.name; // Change 'name' to the appropriate field in your database
          searchResults.appendChild(resultItem);
        });
      }
    })
    .catch(error => console.error('Error searching:', error));
});
