import os
import requests
from pathlib import Path

# --- CONFIGURAÇÕES ---
# Caminho onde estão os seus arquivos .txt
CAMINHO_TXT = r'C:\Users\harah\Videos\Teste\Python\txt'
# Caminho da pasta 'mangas' no seu repositório local
# (Ajuste para o caminho real da pasta do GitHub no seu PC)
CAMINHO_REPOSITORIO = r'C:\Caminho\Para\Seu\Repositorio\Manga-Onn\mangas'

def baixar_imagem(url, pasta_destino, nome_arquivo):
    try:
        resposta = requests.get(url, stream=True, timeout=10)
        if resposta.status_code == 200:
            caminho_completo = os.path.join(pasta_destino, nome_arquivo)
            with open(caminho_completo, 'wb') as f:
                for chunk in resposta.iter_content(1024):
                    f.write(chunk)
            return True
    except Exception as e:
        print(f"Erro ao baixar {url}: {e}")
    return False

def processar_arquivos():
    # Garante que a pasta de destino existe
    if not os.path.exists(CAMINHO_REPOSITORIO):
        os.makedirs(CAMINHO_REPOSITORIO)

    # Lista todos os arquivos .txt na pasta
    arquivos_txt = [f for f in os.listdir(CAMINHO_TXT) if f.endswith('.txt')]

    for nome_txt in arquivos_txt:
        nome_manga = Path(nome_txt).stem  # Nome do arquivo sem o .txt
        pasta_manga = os.path.join(CAMINHO_REPOSITORIO, nome_manga)
        
        if not os.path.exists(pasta_manga):
            os.makedirs(pasta_manga)
            print(f"\nCriando pasta para: {nome_manga}")

        caminho_arquivo_txt = os.path.join(CAMINHO_TXT, nome_txt)
        
        with open(caminho_arquivo_txt, 'r') as file:
            urls = file.readlines()
            
            for i, url in enumerate(urls):
                url = url.strip()
                if url:
                    # Define o nome da imagem (ex: 001.jpg, 002.jpg...)
                    extensao = ".jpg" # Você pode ajustar se souber o formato
                    nome_img = f"{str(i+1).zfill(3)}{extensao}"
                    
                    print(f"Baixando página {i+1} de {nome_manga}...", end="\r")
                    baixar_imagem(url, pasta_manga, nome_img)
        
    print("\n\nProcesso concluído!")

if __name__ == "__main__":
    processar_arquivos()