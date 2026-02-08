// CONFIGURAÇÃO - MUDE AQUI AS SUAS CREDENCIAIS
const ADMIN_EMAIL    = "harahellima@gmail.com";       // ← ALTERE PARA O SEU EMAIL
const ADMIN_PASSWORD = "@KramaCaroline22*";       // ← ALTERE PARA SUA SENHA

// Configurações do repositório GitHub
const BASE_URL = "https://raw.githubusercontent.com/Pecorine125/Manga-Onn/main/";

let currentMangaNumber = 0;
let currentPage = 1;

// Mostra/esconde telas
function showScreen(id) {
  document.querySelectorAll('.screen').forEach(el => el.classList.remove('active'));
  document.getElementById(id).classList.add('active');
}

// Login
function tryLogin() {
  const emailInput = document.getElementById('email');
  const passInput  = document.getElementById('password');

  if (!emailInput || !passInput) {
    alert("Erro: campos de login não encontrados no HTML.");
    return;
  }

  const email    = emailInput.value.trim();
  const password = passInput.value.trim();

  if (email === ADMIN_EMAIL && password === ADMIN_PASSWORD) {
    showScreen('manga-select');
    loadMangaCovers();
  } else {
    alert("Email ou senha incorretos!");
    passInput.value = ''; // limpa a senha em caso de erro
  }
}

// Carrega lista de capas
function loadMangaCovers() {
  const grid = document.getElementById('manga-grid');
  grid.innerHTML = '';

  // Mostra de 0 até 99 (altere se quiser mais ou menos)
  for (let i = 0; i < 100; i++) {
    const div = document.createElement('div');
    div.className = 'manga-card';
    div.innerHTML = `
      <img src="${BASE_URL}capas/${i}.jpg" alt="Manga ${i}"
           onerror="this.src='https://via.placeholder.com/140x180/222/eee?text=${i}';">
      <div style="margin-top:8px; font-size:0.9rem;">${i}</div>
    `;
    div.onclick = () => openManga(i);
    grid.appendChild(div);
  }
}

// Abre tela da capa
function openManga(num) {
  currentMangaNumber = num;
  currentPage = 1;

  const cover = document.getElementById('current-cover');
  cover.src = `${BASE_URL}capas/${num}.jpg`;
  cover.onerror = () => {
    cover.src = "https://via.placeholder.com/400x600/222/eee?text=Sem+capa";
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

// Inicia leitura ao clicar na capa
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
      img.src = "https://via.placeholder.com/800x1200/111/eee?text=Erro";
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
  alert("Fechando o aplicativo...\n\n(Em navegador normal esta ação não fecha a aba)");
}

// Início da aplicação
setTimeout(() => {
  showScreen('login');
}, 1500);