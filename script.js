// ────────────────────────────────────────────────
// CONFIGURAÇÃO - MUDE AQUI AS SUAS CREDENCIAIS
// ────────────────────────────────────────────────
const ADMIN_EMAIL   = "harahellima@gmail.com";          // ← COLOQUE SEU EMAIL AQUI
const ADMIN_PASSWORD = "@AquaMarine22*";      // ← COLOQUE UMA SENHA FORTE AQUI

// ────────────────────────────────────────────────
// Configurações do repositório
// ────────────────────────────────────────────────
const BASE_URL = "https://raw.githubusercontent.com/Pecorine125/Manga-Onn/main/";

let currentMangaNumber = 0;
let currentPage = 1;

// ────────────────────────────────────────────────
function showScreen(id) {
  document.querySelectorAll('.screen').forEach(el => el.classList.remove('active'));
  document.getElementById(id).classList.add('active');
}

// ────────────────────────────────────────────────
function tryLogin() {
  const email    = document.getElementById('email').value.trim();
  const password = document.getElementById('password').value.trim();

  if (email === ADMIN_EMAIL && password === ADMIN_PASSWORD) {
    showScreen('manga-select');
    loadMangaCovers();
  } else {
    alert("Email ou senha incorretos!");
    document.getElementById('password').value = ''; // limpa só a senha
  }
}

// ────────────────────────────────────────────────
function loadMangaCovers() {
  const grid = document.getElementById('manga-grid');
  grid.innerHTML = '';

  // Mostrando de 0 até 99 — altere o número se quiser mais/menos
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

// ────────────────────────────────────────────────
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

// ────────────────────────────────────────────────
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

// ────────────────────────────────────────────────
document.getElementById('current-cover').onclick = function() {
  currentPage = 1;
  loadPage();
  showScreen('reader');
};

// ────────────────────────────────────────────────
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
  // window.close(); // só funciona em janelas abertas por script
}

// ────────────────────────────────────────────────
// Início
// ────────────────────────────────────────────────
setTimeout(() => {
  showScreen('login');
}, 1500);