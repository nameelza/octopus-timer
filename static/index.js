// Make sidebar icon visible on main page load
document.addEventListener("DOMContentLoaded", function () {
  document.querySelector(".todoIcon").style.visibility = "visible";
});

// Timer
const start = document.getElementById("start");
const brk = document.getElementById("break");
const cntn = document.getElementById("continue");
const finish = document.getElementById("finish");

let m;
let s;

let startTime;
let time;
let timerIsOn = 0;
let t;

const FULL_DASH_ARRAY = 293;

start.addEventListener("click", function () {
  m = document.getElementById("minutes");
  s = document.getElementById("seconds");
  startTime = parseInt(m.value, 10) * 60 + parseInt(s.value, 10);

  if (!timerIsOn) {
    timerIsOn = 1;
    t = setInterval(startTimer, 1000);
    start.style.display = "none";
    brk.style.display = "block";
    finish.style.display = "block";
    document.getElementById("minutes").disabled = true;
    document.getElementById("seconds").disabled = true;
    document.getElementById("timerInput").disabled = true;
    if (document.getElementById("timerInput").value === "") {
      document.getElementById("timerInput").value = " ";
    }
  }
});

brk.addEventListener("click", function () {
  timerIsOn = 0;
  clearInterval(t);
  start.style.display = "none";
  brk.style.display = "none";
  finish.style.display = "block";
  cntn.style.display = "block";
});

cntn.addEventListener("click", function () {
  timerIsOn = 1;
  t = setInterval(startTimer, 1000);
  start.style.display = "none";
  brk.style.display = "block";
  finish.style.display = "block";
  cntn.style.display = "none";
});

finish.addEventListener("click", function () {
  timerIsOn = 0;
  submitSession();
  clearInterval(t);
  start.style.display = "block";
  brk.style.display = "none";
  finish.style.display = "none";
  cntn.style.display = "none";
  m.value = "25";
  s.value = "00";
  document.getElementById("minutes").disabled = false;
  document.getElementById("seconds").disabled = false;
  document.querySelector(".circleProgress").style.strokeDasharray="0, 293";
  document.getElementById("timerInput").disabled = false;
  document.getElementById("timerInput").value = "";
  console.log(startTime);
  console.log(time);
});

// Divides time left by the defined time limit.
function calculateTimeFraction() {
  return ((startTime + 0.5 - time) * 293) / startTime;
}

// Update the dasharray value as time passes, starting with 283
function setCircleDasharray() {
  const circleDasharray = `${calculateTimeFraction().toFixed(0)} 293`;
  document.querySelector(".circleProgress").style.strokeDasharray =
    circleDasharray;
}

function startTimer() {
  time = parseInt(m.value, 10) * 60 + parseInt(s.value, 10);
  time--;
  console.log("Run");
  setCircleDasharray();
  let minutes = Math.floor(time / 60);
  let seconds = time % 60;

  if (minutes < 10) {
    m.value = "0" + minutes;
  } else {
    m.value = minutes;
  }

  if (seconds < 10) {
    s.value = "0" + seconds;
  } else {
    s.value = seconds;
  }

  // If time is up, stop the timer and display the start button.
  if (time < 0) {
    timerIsOn = 0;
    clearInterval(t);
    m.value = "00";
    s.value = "00";
  }
}


// Submit session name and duration to database
function submitSession() {
  duration = startTime - time;
  fetch("/", {
    method: "POST",
    body: JSON.stringify({
      name: document.getElementById("timerInput").value,
      duration: duration
    })
  })
}