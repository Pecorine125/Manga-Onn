import os
import requests
import subprocess
from pathlib import Path

# --- CONFIGURAÇÕES ---
# Onde estão os arquivos .txt (Pasta no seu PC)
CAMINHO_TXT = r'C:\Users\harah\Videos\Teste\Python\txt'

# Onde você clonou o seu repositório Manga-Onn
CAMINHO_REPO_LOCAL = r'C:\Users\harah\Documents\Manga-Onn'

def baixar_imagem(url, pasta_destino, nome_arquivo):
    try:
        resposta = requests.get(url, timeout=15)
        if resposta.status_code == 200:
            caminho = os.path.join(pasta_destino, nome_arquivo)
            with open(caminho, 'wb') as f:
                f.write(resposta.content)
            return True
    except:
        return False

def enviar_ao_github():
    print("\n--- Enviando para o GitHub ---")
    try:
        # Adiciona apenas as pastas de capas e mangas
        subprocess.run(["git", "add", "capas/*", "mangas/*"], cwd=CAMINHO_REPO_LOCAL, check=True)
        subprocess.run(["git", "commit", "-m", "Adicionando novos mangas e capas"], cwd=CAMINHO_REPO_LOCAL, check=True)
        subprocess.run(["git", "push", "origin", "main"], cwd=CAMINHO_REPO_LOCAL, check=True)
        print("Upload concluído!")
    except Exception as e:
        print(f"Erro no Git: {e}")

def main():
    pasta_mangas = os.path.join(CAMINHO_REPO_LOCAL, 'mangas')
    pasta_capas = os.path.join(CAMINHO_REPO_LOCAL, 'capas')
    
    # Cria as pastas principais se não existirem
    os.makedirs(pasta_mangas, exist_ok=True)
    os.makedirs(pasta_capas, exist_ok=True)

    arquivos_txt = [f for f in os.listdir(CAMINHO_TXT) if f.endswith('.txt')]
    
    for arquivo in arquivos_txt:
        nome_manga = Path(arquivo).stem
        diretorio_manga = os.path.join(pasta_mangas, nome_manga)
        os.makedirs(diretorio_manga, exist_ok=True)
        
        print(f"\nProcessando: {nome_manga}")
        
        caminho_completo_txt = os.path.join(CAMINHO_TXT, arquivo)
        with open(caminho_completo_txt, 'r') as f:
            urls = [linha.strip() for linha in f.readlines() if linha.strip()]
            
            for i, url in enumerate(urls):
                # 1. Se for a primeira imagem, salva também na pasta 'capas'
                if i == 0:
                    nome_capa = f"Capa_{nome_manga}.jpg"
                    print(f"  > Salvando Capa em /capas...")
                    baixar_imagem(url, pasta_capas, nome_capa)
                
                # 2. Salva a imagem normalmente na pasta do mangá
                nome_img = f"{str(i+1).zfill(3)}.jpg"
                print(f"  > Baixando página {i+1}...", end="\r")
                baixar_imagem(url, diretorio_manga, nome_img)
    
    # Envia as alterações
    enviar_ao_github()

if __name__ == "__main__":
    main()