import os
import requests
import subprocess
import json
from pathlib import Path

# --- CONFIGURAÇÕES ---
# Onde estão os seus arquivos .txt
CAMINHO_TXT = r'C:\Users\harah\Videos\Teste\Python\txt'

# Onde os mangás serão salvos no seu PC (Pasta do Repositório)
CAMINHO_REPO_LOCAL = r'C:\Users\harah\Videos\Teste\Python'

def baixar_imagem(url, pasta_destino, nome_arquivo):
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        resposta = requests.get(url, headers=headers, timeout=15)
        if resposta.status_code == 200:
            caminho = os.path.join(pasta_destino, nome_arquivo)
            with open(caminho, 'wb') as f:
                f.write(resposta.content)
            return True
    except:
        return False

def atualizar_lista_json(pasta_mangas):
    # Cria/Atualiza o mangas.json com o nome das pastas
    mangas = [d for d in os.listdir(pasta_mangas) if os.path.isdir(os.path.join(pasta_mangas, d))]
    with open(os.path.join(CAMINHO_REPO_LOCAL, 'mangas.json'), 'w', encoding='utf-8') as f:
        json.dump(mangas, f, ensure_ascii=False, indent=4)

def enviar_ao_github():
    print("\n--- Iniciando Envio Automático para o GitHub ---")
    try:
        # 1. Garante que está no branch main
        subprocess.run(["git", "branch", "-M", "main"], cwd=CAMINHO_REPO_LOCAL)
        # 2. Adiciona as mudanças (capas, mangas e json)
        subprocess.run(["git", "add", "."], cwd=CAMINHO_REPO_LOCAL, check=True)
        # 3. Cria o commit
        subprocess.run(["git", "commit", "-m", "Auto-update: Mangas e Capas"], cwd=CAMINHO_REPO_LOCAL, check=True)
        # 4. Faz o push
        subprocess.run(["git", "push", "origin", "main"], cwd=CAMINHO_REPO_LOCAL, check=True)
        print(">>> SUCESSO: Tudo enviado para o GitHub!")
    except Exception as e:
        print(f">>> ERRO no Git: {e}")

def main():
    pasta_mangas = os.path.join(CAMINHO_REPO_LOCAL, 'mangas')
    pasta_capas = os.path.join(CAMINHO_REPO_LOCAL, 'capas')
    
    os.makedirs(pasta_mangas, exist_ok=True)
    os.makedirs(pasta_capas, exist_ok=True)

    arquivos_txt = [f for f in os.listdir(CAMINHO_TXT) if f.endswith('.txt')]
    
    if not arquivos_txt:
        print(f"Nenhum arquivo .txt em: {CAMINHO_TXT}")
        return

    for arquivo in arquivos_txt:
        nome_manga = Path(arquivo).stem
        diretorio_manga = os.path.join(pasta_mangas, nome_manga)
        os.makedirs(diretorio_manga, exist_ok=True)
        
        print(f"\nProcessando: {nome_manga}")
        
        with open(os.path.join(CAMINHO_TXT, arquivo), 'r') as f:
            urls = [l.strip() for l in f.readlines() if l.strip()]
            
            for i, url in enumerate(urls):
                # Salva a primeira como Capa (Nome do arquivo)
                if i == 0:
                    baixar_imagem(url, pasta_capas, f"{nome_manga}.jpg")
                
                # Salva as páginas (001, 002...)
                nome_img = f"{str(i+1).zfill(3)}.jpg"
                baixar_imagem(url, diretorio_manga, nome_img)
                print(f"  > Baixando {i+1} de {len(urls)}", end="\r")

    # Atualiza o arquivo de lista para o seu futuro site
    atualizar_lista_json(pasta_mangas)
    
    # Envia tudo para o GitHub
    enviar_ao_github()

if __name__ == "__main__":
    main()