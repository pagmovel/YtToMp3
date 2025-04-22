import yt_dlp
import os
import zipfile
import requests
from tqdm import tqdm
import glob

def find_ffmpeg_executables(ffmpeg_dir):
    """Procura recursivamente pelos executáveis do FFmpeg em qualquer subdiretório"""
    pattern = '**' + os.path.sep + '*ff*.exe' if os.name == 'nt' else '**' + os.path.sep + '*ff*'
    matches = glob.glob(os.path.join(ffmpeg_dir, pattern), recursive=True)
    return matches

def get_ffmpeg_bin_dir():
    """Retorna o diretório que contém os executáveis do FFmpeg"""
    ffmpeg_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ffmpeg')
    executables = find_ffmpeg_executables(ffmpeg_dir)
    
    if executables:
        # Pega o diretório do primeiro executável encontrado
        return os.path.dirname(executables[0])
    return ffmpeg_dir

def download_ffmpeg():
    ffmpeg_url = "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip"
    ffmpeg_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ffmpeg')
    
    if not os.path.exists(ffmpeg_dir):
        os.makedirs(ffmpeg_dir)
        
    print("Baixando FFmpeg...")
    response = requests.get(ffmpeg_url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    
    zip_path = os.path.join(ffmpeg_dir, "ffmpeg.zip")
    with open(zip_path, 'wb') as file, tqdm(
        desc="Progresso",
        total=total_size,
        unit='iB',
        unit_scale=True,
        unit_divisor=1024,
    ) as pbar:
        for data in response.iter_content(chunk_size=1024):
            size = file.write(data)
            pbar.update(size)
    
    print("Extraindo arquivos...")
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(ffmpeg_dir)
    
    os.remove(zip_path)
    print("FFmpeg instalado com sucesso!")

def check_ffmpeg():
    executables = find_ffmpeg_executables(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ffmpeg'))
    required_names = ['ffmpeg', 'ffplay', 'ffprobe']
    
    # Verifica se todos os executáveis necessários existem
    has_all_required = all(
        any(req in os.path.basename(exe).lower() for exe in executables)
        for req in required_names
    )
    
    if not has_all_required:
        print("FFmpeg não encontrado. Baixando...")
        download_ffmpeg()

def convert_to_mp3(links_file):
    if not os.path.exists('downloads'):
        os.makedirs('downloads')

    ffmpeg_bin_dir = get_ffmpeg_bin_dir()
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320',
        }],
        'outtmpl': os.path.join('downloads', '%(title)s.%(ext)s'),
        'ffmpeg_location': ffmpeg_bin_dir
    }

    try:
        with open(links_file, 'r') as file:
            links = [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        print(f"Erro: Arquivo '{links_file}' não encontrado.")
        return

    for link in links:
        try:
            print(f"\nProcessando: {link}")
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([link])
        except Exception as e:
            print(f"Erro processando {link}: {str(e)}")

if __name__ == "__main__":
    check_ffmpeg()  # Verifica e baixa o FFmpeg se necessário
    links_file = "links.txt"
    convert_to_mp3(links_file)
    print("\nConversão concluída!")