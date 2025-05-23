import argparse
import glob
import logging
from ftplib import FTP
from pathlib import Path

from mp3_util import MP3Transformer


def move_files(mp3s: list, destination_folder_path: str) -> list:

    new_file_paths = []
    logger.info(f"Attempting to move {len(mp3s)} file(s).")
    for mp3f in mp3s:
        new_file_name = Path(destination_folder_path) / Path(mp3f).name
        logger.info(f"Moving file to destination: {new_file_name}")
        Path(mp3f).rename(new_file_name)
        new_file_paths.append(new_file_name)
        
    return new_file_paths

def send_to_phone(url:str, port:str, list_of_files) -> None:

    ftp = FTP()
    ftp.connect(url, int(port))
    ftp.login('android', 'android')

    for file in list_of_files:
        logger.info(f"Sending {file}")
        with open(file, 'rb') as f:
            ftp.storbinary(f'STOR Music/{Path(file).name}', f)
    
    quit()

if __name__ == "__main__":

    # Variables
    downloads_folder_path = Path.home() / 'Downloads'
    destination_folder_path = Path.home() / 'Music' / 'Canciones' / 'Otros'
    cover_art_path = Path.home() / 'Pictures' / 'Imagenes' / 'Varias' / 'Others.png'
    
    # Arguments
    parser = argparse.ArgumentParser(
        description="This script moves the mp3s on your downloads folder to you music folders' loosies subfolder. " \
        "It also removes some of its metadata in the process and finally sends the processed files to your phone."
    )
    parser.add_argument("-v", '--verbose', action="store_true", help="Specifies extra print output for debug purposes.")
    args = parser.parse_args()

    # Logging set-up according to arguments
    logger = logging.getLogger(__name__)
    logging_level = 0
    if args.verbose:
        logging_level = logging.DEBUG
        logging.basicConfig(level=logging_level)

    # MP3 Changer
    list_of_mp3s = glob.glob(rf'{downloads_folder_path}\*.mp3')
    mp3_transformer = MP3Transformer(list_of_mp3s, logging_level)
    mp3_transformer.change_attributes(str(cover_art_path))
    
    # Move files to folder locally and to phone
    new_file_paths = move_files(list_of_mp3s, str(destination_folder_path))
    url = input("Please start your FTP server and enter your IP: ")
    port = input("Please specify the opened port for your FTP server: ")
    send_to_phone(url, port, new_file_paths)
