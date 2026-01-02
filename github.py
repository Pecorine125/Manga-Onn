import os
import requests
import subprocess
from pathlib import Path

# --- CONFIGURAÇÕES ---
CAMINHO_TXT = r'C:\Users\harah\Videos\Teste\Python\txt'
CAMINHO_REPO_LOCAL = r'C:\Users\harah\Videos\Teste\Python'

def baixar_imagem(url, pasta_destino, nome_arquivo):
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        resposta = requests.get(url, headers=headers, timeout=15)
        if resposta.status_code == 200:
            with open(os.path.join(pasta_destino, nome_arquivo), 'wb') as f:
                f.write(resposta.content)
            return True
    except: return False

def enviar_ao_github():
    print("\n--- Enviando Pastas para o GitHub ---")
    try:
        # 1. Configura o branch
        subprocess.run(["git", "branch", "-M", "main"], cwd=CAMINHO_REPO_LOCAL)
        
        # 2. Adiciona APENAS as pastas desejadas para garantir
        subprocess.run(["git", "add", "capas/", "mangas/"], cwd=CAMINHO_REPO_LOCAL, check=True)
        
        # 3. Commit
        subprocess.run(["git", "commit", "-m", "Upload: Apenas capas e mangas"], cwd=CAMINHO_REPO_LOCAL)
        
        # 4. Push Forçado para resolver o erro anterior (rejected)
        print("  > Forçando atualização do repositório...")
        subprocess.run(["git", "push", "origin", "main", "--force"], cwd=CAMINHO_REPO_LOCAL, check=True)
        print(">>> SUCESSO: Pastas enviadas!")
    except Exception as e:
        print(f">>> Erro no Git: {e}")

def main():
    pasta_mangas = os.path.join(CAMINHO_REPO_LOCAL, 'mangas')
    pasta_capas = os.path.join(CAMINHO_REPO_LOCAL, 'capas')
    os.makedirs(pasta_mangas, exist_ok=True)
    os.makedirs(pasta_capas, exist_ok=True)

    arquivos_txt = [f for f in os.listdir(CAMINHO_TXT) if f.endswith('.txt')]
    
    for arquivo in arquivos_txt:
        nome_manga = Path(arquivo).stem
        diretorio_manga = os.path.join(pasta_mangas, nome_manga)
        os.makedirs(diretorio_manga, exist_ok=True)
        
        print(f"\nBaixando: {nome_manga}")
        with open(os.path.join(CAMINHO_TXT, arquivo), 'r') as f:
            urls = [l.strip() for l in f.readlines() if l.strip()]
            for i, url in enumerate(urls):
                if i == 0: baixar_imagem(url, pasta_capas, f"{nome_manga}.jpg")
                baixar_imagem(url, diretorio_manga, f"{str(i+1).zfill(3)}.jpg")
                print(f"  > Pagina {i+1}/{len(urls)}", end="\r")

    enviar_ao_github()

if __name__ == "__main__":
    main()