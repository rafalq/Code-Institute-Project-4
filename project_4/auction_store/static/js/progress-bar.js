// Use the end_date from the Item django model
var endDate = document.getElementById("timer").innerHTML;

// Set the date we're counting down to
var countDownDate = new Date(endDate).getTime();
var tday = new Date().getTime();

var timeLeft = Math.floor((countDownDate - tday) / 1000);
var progressNow = Math.floor((timeLeft * 100) / timeFromStart);

//change for a string to be able to use as an arg in the functions
var secondsStr = timeLeft + "s";

var progressBar = document.getElementById("progress-bar");

addEventListener('load', function() {
  progressBar.style.transitionDuration = secondsStr;
  progressBar.style.width = '0%';
  progressBar.style["background-color"] = '#ffc107';
});
