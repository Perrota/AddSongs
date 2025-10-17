import argparse
import json
import logging
from ftplib import FTP
from pathlib import Path

from prompt_toolkit import prompt

from mp3_util import MP3Transformer


def move_files(mp3s: list[Path], destination_folder_path: str) -> list[str]:

    new_file_paths = []
    logger.info(f"Attempting to move {len(mp3s)} file(s).")
    for mp3f in mp3s:
        new_file_name = Path(destination_folder_path) / mp3f.name
        logger.info(f"Moving file to destination: {new_file_name}")
        mp3f.rename(new_file_name)
        new_file_paths.append(str(new_file_name))
        
    return new_file_paths

def send_to_phone(url:str, port:str, list_of_files:list[str]) -> None:

    ftp = FTP()
    try:
        ftp.connect(url, int(port))
        ftp.login('android', 'android')
    except Exception as e:
        logger.error(f"Failed to connect to FTP server at {url}:{port}. Error: {e}")
        return

    for file in list_of_files:
        logger.info(f"Sending {file}")
        with open(file, 'rb') as f:
            ftp.storbinary(f'STOR Music/{Path(file).name}', f)

def save_cache(data:dict, cache_path:Path, server_address:str, port:str) -> None:
    if data.get("server_address", "") != server_address or data.get("port", "") != port:
        data["server_address"] = server_address
        data["port"] = port
    with cache_path.open('w', encoding='utf-8') as f:
        json.dump(data, f)

if __name__ == "__main__":

    # Variables
    downloads_folder_path = Path.home() / 'Downloads'
    destination_folder_path = Path.home() / 'Music' / 'Canciones' / 'Otros'
    cover_art_path = Path.home() / 'Pictures' / 'Imagenes' / 'Varias' / 'Others.png'
    
    # Cache
    cache_path = Path('cache.json')
    with cache_path.open('r', encoding='utf-8') as f:
        cache = json.load(f)

    # Arguments
    parser = argparse.ArgumentParser(
        description="This script moves the mp3s on your downloads folder to you music folders' loosies subfolder. " \
        "It also removes some of its metadata in the process and finally sends the processed files to your phone."
    )
    parser.add_argument("-v", '--verbose', action="store_true", help="Specifies extra print output for debug purposes.")
    args = parser.parse_args()

    # Logging set-up according to arguments
    logging_level = logging.DEBUG if args.verbose else logging.WARNING
    logging.basicConfig(level=logging_level)
    logger = logging.getLogger(__name__)

    # MP3 Changer
    list_of_mp3s = list(downloads_folder_path.glob("*.mp3"))
    mp3_transformer = MP3Transformer(list_of_mp3s)
    mp3_transformer.change_attributes(str(cover_art_path))
    
    # Move files to folder locally and to phone
    new_file_paths = move_files(list_of_mp3s, str(destination_folder_path))
    if new_file_paths:
        url = prompt("Please start your FTP server and enter your IP: ", default=cache.get("server_address", ""))
        port = prompt("Please specify the opened port for your FTP server: ", default=cache.get("port", ""))
        save_cache(cache, cache_path, url, port)
        send_to_phone(url, port, new_file_paths)
