import os
import requests
from pathlib import Path

# --- CONFIGURAÇÕES ---
# Onde estão os seus arquivos .txt
CAMINHO_TXT = r'C:\Users\harah\Videos\Teste\Python\txt'

# Onde os mangás serão salvos no seu PC (Diretório do seu projeto)
# IMPORTANTE: Use o caminho da pasta no seu Windows, não o link do GitHub.
CAMINHO_DESTINO = r'C:\Users\harah\Videos\Teste\Python'

def baixar_imagem(url, pasta_destino, nome_arquivo):
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        resposta = requests.get(url, headers=headers, timeout=15)
        if resposta.status_code == 200:
            caminho_completo = os.path.join(pasta_destino, nome_arquivo)
            with open(caminho_completo, 'wb') as f:
                f.write(resposta.content)
            return True
    except:
        return False

def main():
    # Define e cria as pastas 'mangas' e 'capas' no seu diretório
    pasta_mangas_base = os.path.join(CAMINHO_DESTINO, 'mangas')
    pasta_capas_base = os.path.join(CAMINHO_DESTINO, 'capas')
    
    os.makedirs(pasta_mangas_base, exist_ok=True)
    os.makedirs(pasta_capas_base, exist_ok=True)

    # Localiza todos os arquivos .txt na pasta de origem
    arquivos_txt = [f for f in os.listdir(CAMINHO_TXT) if f.endswith('.txt')]
    
    if not arquivos_txt:
        print(f"Nenhum arquivo .txt encontrado em: {CAMINHO_TXT}")
        return

    for arquivo in arquivos_txt:
        nome_do_manga = Path(arquivo).stem  # Pega o nome do arquivo (ex: "Naruto")
        
        # Cria a pasta específica do mangá dentro de 'mangas'
        pasta_manga_final = os.path.join(pasta_mangas_base, nome_do_manga)
        os.makedirs(pasta_manga_final, exist_ok=True)
        
        print(f"\nIniciando: {nome_do_manga}")
        
        caminho_arquivo_txt = os.path.join(CAMINHO_TXT, arquivo)
        with open(caminho_arquivo_txt, 'r') as f:
            urls = [linha.strip() for linha in f.readlines() if linha.strip()]
            
            for i, url in enumerate(urls):
                # 1. Primeira imagem vira a Capa na pasta 'capas'
                if i == 0:
                    nome_capa = f"{nome_do_manga}.jpg"
                    baixar_imagem(url, pasta_capas_base, nome_capa)
                    print(f"  > Capa salva com sucesso.")
                
                # 2. Todas as imagens vão para a pasta do mangá (001.jpg, 002.jpg...)
                nome_imagem = f"{str(i+1).zfill(3)}.jpg"
                baixar_imagem(url, pasta_manga_final, nome_imagem)
                print(f"  > Baixando página {i+1} de {len(urls)}...", end="\r")

    print("\n\nDownload concluído! Agora você pode usar o 'git push' manualmente.")

if __name__ == "__main__":
    main()