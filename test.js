document.getElementById('addEvent').addEventListener('click', function() {
  var timeline = document.getElementById('timeline');
  var newEventYear = prompt("Enter the year of the event:");
  var newEventTitle = prompt("Enter the title of the event:");
  var newEventDescription = prompt("Enter the description of the event:");

  var timelineItem = document.createElement('div');
  timelineItem.classList.add('timeline-item');

  var timelineDate = document.createElement('div');
  timelineDate.classList.add('timeline-date');
  timelineDate.textContent = newEventYear;

  var timelineContent = document.createElement('div');
  timelineContent.classList.add('timeline-content');
  timelineContent.innerHTML = '<h3>' + newEventTitle + '</h3>' + '<p>' + newEventDescription + '</p>';

  timelineItem.appendChild(timelineDate);
  timelineItem.appendChild(timelineContent);
  timeline.appendChild(timelineItem);
});
