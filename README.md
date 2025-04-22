# YouTube to MP3 Converter

Conversor simples de vídeos do YouTube para arquivos MP3.

## Requisitos

- Python 3.6 ou superior
- pip (gerenciador de pacotes do Python)

## Instalação

1. Clone este repositório:

```bash
git clone https://github.com/pagmovel/YtToMp3.git
cd YtToMp3
```

2. Crie e ative um ambiente virtual:

```bash
python -m venv venv
venv\Scripts\activate
```

3. Instale as dependências:

```bash
pip install -r requirements.txt
```

## Uso

1. Adicione os links do YouTube ao arquivo `links.txt`, um por linha.

2. Execute o script:

```bash
python youtube_to_mp3.py
```

O script irá:

- Baixar o FFmpeg automaticamente na primeira execução (se necessário)
- Criar uma pasta 'downloads' se ela não existir
- Converter cada vídeo para MP3 e salvá-lo na pasta 'downloads'

## Notas

- O FFmpeg será baixado automaticamente na primeira execução
- Os arquivos MP3 serão salvos na pasta 'downloads'
- Qualidade do áudio: 320kbps
