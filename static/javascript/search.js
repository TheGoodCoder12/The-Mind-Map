document.addEventListener('DOMContentLoaded', function() {
  const searchType = document.getElementById('searchType')
  const dateChosen = document.getElementById('dateChosen')
  const peopleChosen = document.getElementById('peopleChosen')
  const cluesChosen = document.getElementById('cluesChosen')

  searchType.addEventListener('change', function() {
    if (this.value == 'date') {
      dateChosen.classList.remove('hidden');
      peopleChosen.classList.add('hidden');
      cluesChosen.classList.add('hidden');
    }
    else if (this.value == 'people') {
      dateChosen.classList.add('hidden');
      peopleChosen.classList.remove('hidden');
      cluesChosen.classList.add('hidden');
    }
    else if (this.value == 'clues') {
      dateChosen.classList.add('hidden');
      peopleChosen.classList.add('hidden');
      cluesChosen.classList.remove('hidden');
    }
  });
});