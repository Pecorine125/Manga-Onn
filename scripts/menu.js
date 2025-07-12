const slider = document.getElementById("slider");
const totalCapas = 10;
let currentIndex = 0;

// Carrega as imagens no slider
for (let i = 0; i < totalCapas; i++) {
  const img = document.createElement("img");
  img.src = `../capas/Capa ${i}.jpg`;
  img.className = "capa flex-shrink-0 w-full h-full cursor-pointer";
  img.onclick = () => {
    localStorage.setItem("mangaSelecionado", i);
    window.location.href = "viewer.html";
  };
  slider.appendChild(img);
}

function updateSlider() {
  slider.style.transform = `translateX(-${currentIndex * 100}%)`;
}

function next() {
  if (currentIndex < totalCapas - 1) {
    currentIndex++;
    updateSlider();
  }
}

function prev() {
  if (currentIndex > 0) {
    currentIndex--;
    updateSlider();
  }
}

// Swipe com touch (mobile)
let startX = 0;
slider.addEventListener("touchstart", e => startX = e.touches[0].clientX);
slider.addEventListener("touchend", e => {
  const endX = e.changedTouches[0].clientX;
  if (endX < startX - 50) next();
  else if (endX > startX + 50) prev();
});

function closeApp() {
  window.close();
}
