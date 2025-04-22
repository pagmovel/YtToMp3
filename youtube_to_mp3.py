import yt_dlp
import os
import zipfile
import requests
from tqdm import tqdm

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
        for file in zip_ref.namelist():
            if file.endswith(('.exe', '.dll')) and not file.startswith('_'):
                zip_ref.extract(file, ffmpeg_dir)
    
    os.remove(zip_path)
    print("FFmpeg instalado com sucesso!")

def check_ffmpeg():
    ffmpeg_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ffmpeg')
    required_files = ['ffmpeg.exe', 'ffplay.exe', 'ffprobe.exe']
    
    if not all(os.path.exists(os.path.join(ffmpeg_dir, file)) for file in required_files):
        print("FFmpeg não encontrado. Baixando...")
        download_ffmpeg()

def convert_to_mp3(links_file):
    if not os.path.exists('downloads'):
        os.makedirs('downloads')

    ffmpeg_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ffmpeg')
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320',
        }],
        'outtmpl': os.path.join('downloads', '%(title)s.%(ext)s'),
        'ffmpeg_location': ffmpeg_dir
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