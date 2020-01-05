/*
 *  Creates a progressbar.
 *  @param id the id of the div we want to transform in a progressbar
 *  @param duration the duration of the timer example: '10s'
 *  @param callback, optional function which is called when the progressbar reaches 0.
 */
 // Use the end_date from the Item django model
var endDate = document.getElementById("timer").innerHTML;
// Set the date we're counting down to
var countDownDate = new Date(endDate).getTime();

var tday = new Date().getTime();
//change the end_date for seconds
var seconds = Math.floor((countDownDate - tday) / 1000);
//change for a string to be able to use as an arg in createProgressbar function
var secondsStr = seconds + "s";

function createProgressbar(id, duration, callback) {
  // We select the div that we want to turn into a progressbar
  var progressbar = document.getElementById(id);
  progressbar.className = 'progressbar';

  // We create the div that changes width to show progress
  var progressbarinner = document.createElement('div');
  progressbarinner.className = 'inner';

  // Now we set the animation parameters
  progressbarinner.style.animationDuration = duration;

  // Eventually couple a callback
  if (typeof(callback) === 'function') {
    progressbarinner.addEventListener('animationend', callback);
  }

  // Append the progressbar to the main progressbardiv
  progressbar.appendChild(progressbarinner);

  // When everything is set up we start the animation
  progressbarinner.style.animationPlayState = 'running';
}

addEventListener('load', function() {
  createProgressbar('progressbar', secondsStr, function() {
    alert('Time is up!');
  });
});
