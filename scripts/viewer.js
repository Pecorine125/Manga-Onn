const pasta = localStorage.getItem("mangaSelecionado");
let pagina = 0;
let totalPaginas = 0;

function atualizarImagem() {
  document.getElementById("manga-img").src = `../mangas/${pasta}/Imagens ${pagina}.jpg`;
}

async function verificarTotalPaginas() {
  for (let i = 0; i < 999; i++) {
    const img = new Image();
    img.src = `../mangas/${pasta}/Imagens ${i}.jpg`;

    await new Promise(resolve => {
      img.onload = () => {
        totalPaginas = i + 1;
        resolve();
      };
      img.onerror = resolve;
    });

    if (img.naturalWidth === 0) break;
  }
  atualizarImagem();
}

function proxima() {
  if (pagina + 1 < totalPaginas) {
    pagina++;
    atualizarImagem();
  } else {
    alert("Última página!");
  }
}

function anterior() {
  if (pagina > 0) {
    pagina--;
    atualizarImagem();
  } else {
    alert("Primeira página!");
  }
}

function voltarMenu() {
  window.location.href = "menu.html";
}

function closeApp() {
  window.close();
}

verificarTotalPaginas();
