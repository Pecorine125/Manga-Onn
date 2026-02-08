// Configurações
const BASE_URL = "https://raw.githubusercontent.com/Pecorine125/Manga-Onn/main/";

let currentMangaNumber = 0;
let currentPage = 1;

// Funções de navegação entre telas
function showScreen(id) {
  document.querySelectorAll('.screen').forEach(el => el.classList.remove('active'));
  document.getElementById(id).classList.add('active');
}

// Login (simples / qualquer usuário entra)
function tryLogin() {
  const user = document.getElementById('username').value.trim();
  if (user.length > 0) {
    showScreen('manga-select');
    loadMangaCovers();
  } else {
    alert("Digite um nome de usuário");
  }
}

// Carrega as capas (0 a 59 — altere o limite se quiser)
function loadMangaCovers() {
  const grid = document.getElementById('manga-grid');
  grid.innerHTML = '';

  for (let i = 0; i < 60; i++) {
    const div = document.createElement('div');
    div.className = 'manga-card';
    div.innerHTML = `
      <img src="${BASE_URL}capas/${i}.jpg" alt="Manga ${i}"
           onerror="this.src='https://via.placeholder.com/140x180?text=?';">
      <div style="margin-top:6px;">${i}</div>
    `;
    div.onclick = () => openManga(i);
    grid.appendChild(div);
  }
}

// Abre a tela da capa do mangá selecionado
function openManga(num) {
  currentMangaNumber = num;
  currentPage = 1;

  const cover = document.getElementById('current-cover');
  cover.src = `${BASE_URL}capas/${num}.jpg`;
  cover.onerror = () => {
    cover.src = "https://via.placeholder.com/300x450?text=Sem+capa";
  };

  showScreen('cover-view');
}

// Navegação entre capas
function prevManga() {
  if (currentMangaNumber > 0) {
    currentMangaNumber--;
    openManga(currentMangaNumber);
  }
}

function nextManga() {
  currentMangaNumber++;
  openManga(currentMangaNumber);
}

// Inicia a leitura (clique na capa)
document.getElementById('current-cover').onclick = function() {
  currentPage = 1;
  loadPage();
  showScreen('reader');
};

// Carrega página do mangá
function loadPage() {
  const img = document.getElementById('reader-img');
  const padded = String(currentPage).padStart(3, '0');
  img.src = `${BASE_URL}mangas/${currentMangaNumber}/${padded}.jpg`;

  img.onload = () => {
    document.getElementById('page-number').textContent = `Página ${currentPage}`;
  };

  img.onerror = () => {
    if (currentPage > 1) {
      currentPage--;
      loadPage();
      alert("Fim do capítulo (ou página não encontrada)");
    } else {
      img.src = "https://via.placeholder.com/800x1200?text=Erro+ao+carregar";
    }
  };
}

function nextPage() {
  currentPage++;
  loadPage();
}

function prevPage() {
  if (currentPage > 1) {
    currentPage--;
    loadPage();
  }
}

function backToMangaSelect() {
  showScreen('manga-select');
}

function closeApp() {
  alert("Fechando aplicativo...\n\n(Em navegador real window.close() só funciona em janelas abertas por script)");
  // window.close(); // descomente se estiver em popup/janela controlada
}

// Início da aplicação
setTimeout(() => {
  showScreen('login');
}, 1800);