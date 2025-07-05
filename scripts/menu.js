const menu = document.getElementById("menu");
const totalCapas = 10;

for (let i = 0; i < totalCapas; i++) {
  const img = document.createElement("img");
  img.src = `../capas/Capa ${i}.jpg`;
  img.className = "capa w-36 h-auto cursor-pointer";
  img.onclick = () => {
    localStorage.setItem("mangaSelecionado", i);
    window.location.href = "viewer.html";
  };
  menu.appendChild(img);
}

function closeApp() {
  window.close();
}
