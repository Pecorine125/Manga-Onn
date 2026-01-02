import os
import requests
import subprocess
import json
from pathlib import Path

# --- CONFIGURAÇÕES ---
# Onde estão os seus arquivos .txt
CAMINHO_TXT = r'C:\Users\harah\Videos\Teste\Python\txt'

# Pasta do seu repositório no PC (Onde está o arquivo .git)
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
    # Lista apenas os nomes das pastas dentro de 'mangas'
    mangas = [d for d in os.listdir(pasta_mangas) if os.path.isdir(os.path.join(pasta_mangas, d))]
    with open(os.path.join(CAMINHO_REPO_LOCAL, 'mangas.json'), 'w', encoding='utf-8') as f:
        json.dump(mangas, f, ensure_ascii=False, indent=4)

def enviar_ao_github():
    print("\n--- Sincronizando com GitHub (Estrutura da Imagem 2) ---")
    try:
        # 1. Garante que o Git ignore pastas fantasmas e use a raiz
        subprocess.run(["git", "add", "."], cwd=CAMINHO_REPO_LOCAL, check=True)
        
        # 2. Commit com a mensagem da imagem
        subprocess.run(["git", "commit", "-m", "Auto-upload: Novo manga e capa"], cwd=CAMINHO_REPO_LOCAL, check=True)
        
        # 3. Envio para o branch main
        subprocess.run(["git", "push", "origin", "main"], cwd=CAMINHO_REPO_LOCAL, check=True)
        print(">>> SUCESSO: Repositório atualizado!")
    except Exception as e:
        print(f">>> Erro no processo Git: {e}")

def main():
    # Caminhos absolutos para evitar pastas duplicadas
    pasta_mangas = os.path.join(CAMINHO_REPO_LOCAL, 'mangas')
    pasta_capas = os.path.join(CAMINHO_REPO_LOCAL, 'capas')
    
    os.makedirs(pasta_mangas, exist_ok=True)
    os.makedirs(pasta_capas, exist_ok=True)

    arquivos_txt = [f for f in os.listdir(CAMINHO_TXT) if f.endswith('.txt')]
    
    for arquivo in arquivos_txt:
        nome_manga = Path(arquivo).stem
        diretorio_manga = os.path.join(pasta_mangas, nome_manga)
        os.makedirs(diretorio_manga, exist_ok=True)
        
        print(f"\nProcessando Mangá: {nome_manga}")
        
        with open(os.path.join(CAMINHO_TXT, arquivo), 'r') as f:
            urls = [l.strip() for l in f.readlines() if l.strip()]
            
            for i, url in enumerate(urls):
                # Salva a Capa com o nome do arquivo
                if i == 0:
                    baixar_imagem(url, pasta_capas, f"{nome_manga}.jpg")
                
                # Salva a página na pasta do mangá
                nome_img = f"{str(i+1).zfill(3)}.jpg"
                baixar_imagem(url, diretorio_manga, nome_img)
                print(f"  > Baixando {i+1}/{len(urls)}", end="\r")

    # Gera o JSON na raiz do repositório
    atualizar_lista_json(pasta_mangas)
    
    # Envia tudo
    enviar_ao_github()

if __name__ == "__main__":
    main()