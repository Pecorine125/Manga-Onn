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
            caminho_completo = os.path.join(pasta_destino, nome_arquivo)
            # O modo 'wb' substitui o arquivo automaticamente se ele já existir
            with open(caminho_completo, 'wb') as f:
                f.write(resposta.content)
            return True
    except: return False

def enviar_ao_github():
    print("\n--- Enviando atualizações ao GitHub ---")
    try:
        # Adiciona as pastas (novas ou modificadas)
        subprocess.run(["git", "add", "capas/", "mangas/"], cwd=CAMINHO_REPO_LOCAL, check=True)
        
        # Faz o commit (mesmo que seja substituição, o Git entende como modificação)
        subprocess.run(["git", "commit", "-m", "Atualizacao: Arquivos substituidos ou adicionados"], cwd=CAMINHO_REPO_LOCAL)

        # Envia para a nuvem
        subprocess.run(["git", "push", "origin", "main"], cwd=CAMINHO_REPO_LOCAL, check=True)
        print(">>> SUCESSO: Repositório atualizado no GitHub!")
    except Exception as e:
        print(f">>> Erro no envio: {e}")

def main():
    # --- COMANDO EXECUTADO ANTES DE TUDO ---
    print("--- Sincronizando com o servidor (Pull) ---")
    try:
        # Puxa as mudanças do GitHub para evitar o erro 'rejected'
        subprocess.run(["git", "pull", "origin", "main", "--rebase"], cwd=CAMINHO_REPO_LOCAL)
    except Exception as e:
        print(f"Aviso na sincronização: {e}")

    pasta_mangas = os.path.join(CAMINHO_REPO_LOCAL, 'mangas')
    pasta_capas = os.path.join(CAMINHO_REPO_LOCAL, 'capas')
    
    os.makedirs(pasta_mangas, exist_ok=True)
    os.makedirs(pasta_capas, exist_ok=True)

    arquivos_txt = [f for f in os.listdir(CAMINHO_TXT) if f.endswith('.txt')]
    
    for arquivo in arquivos_txt:
        nome_manga = Path(arquivo).stem
        diretorio_manga = os.path.join(pasta_mangas, nome_manga)
        
        # Cria a pasta se não existir, se existir, apenas continua
        os.makedirs(diretorio_manga, exist_ok=True)
        
        print(f"\nProcessando: {nome_manga} (Substituindo se já existir)")
        with open(os.path.join(CAMINHO_TXT, arquivo), 'r') as f:
            urls = [l.strip() for l in f.readlines() if l.strip()]
            for i, url in enumerate(urls):
                # Substitui a capa
                if i == 0: 
                    baixar_imagem(url, pasta_capas, f"{nome_manga}.jpg")
                
                # Substitui a página
                nome_img = f"{str(i+1).zfill(3)}.jpg"
                baixar_imagem(url, diretorio_manga, nome_img)
                print(f"  > Pagina {i+1}/{len(urls)} processada", end="\r")

    enviar_ao_github()

if __name__ == "__main__":
    main()