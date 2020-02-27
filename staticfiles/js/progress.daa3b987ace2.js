if(document.getElementById("timer").innerHTML != null){
// Use the end_date from the Item django model
var endDate = document.getElementById("timer").innerHTML;
var startDate = document.getElementById("start-date").innerHTML;

// Set the date we're counting down to
var countDownDate = new Date(endDate).getTime();
var startCountDownDate = new Date(startDate).getTime();
var tday = new Date().getTime();

//change the times for seconds
var timeFromStart = Math.floor((countDownDate - startCountDownDate)/ 1000);
var timeLeft = Math.floor((countDownDate - tday) / 1000);
//count the percentage to be able to use it for the progress bar
var progressNow = Math.floor((timeLeft * 100) / timeFromStart) ;

//change for a string to be able to use as an arg in the functions
var progressStr = progressNow + "%";
var progressBar = document.getElementById("progress-bar")
progressBar.style.width = progressStr;
}

var fixedAmountBtn = document.getElementsByClassName("fixed-btn")
var amountInput = document.getElementById("id_amount")

for(var i = 0; i < fixedAmountBtn.length; i++){
  fixedAmountBtn[i].addEventListener("click", function(){
  var btnStr = this.textContent;
  var x = btnStr.split(" ");
  var bidAmount = parseInt(x[7])
  amountInput.value = bidAmount;
  });
}
