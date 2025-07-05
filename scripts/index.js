const bar = document.getElementById("progress-bar");
const text = document.getElementById("progress-text");

let percent = 0;

const loadingInterval = setInterval(() => {
  percent += Math.random() * 8;
  if (percent >= 100) {
    percent = 100;
    clearInterval(loadingInterval);
    setTimeout(() => {
      window.location.href = "html/login.html";
    }, 1000);
  }
  bar.style.width = percent + "%";
  text.textContent = Math.floor(percent) + "%";
}, 300);
