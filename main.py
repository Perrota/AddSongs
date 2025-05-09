import glob
import os
import logging
import argparse
from programs import AirDroid
from mp3_util import MP3Transformer

def move_files(mp3s: list, destination_folder_path: str):

    new_file_paths = []
    logger.info(f"Attempting to move {len(mp3s)} file(s).")
    for mp3f in mp3s:
        new_file_name = os.path.join(destination_folder_path, os.path.basename(mp3f))
        logger.info(f"Moving file to destination: {new_file_name}")
        os.rename(mp3f, new_file_name)
        new_file_paths.append(new_file_name)
        
    return new_file_paths

if __name__ == "__main__":

    # Environ default name
    user_profile = os.environ.get("USERPROFILE")

    # Variables
    downloads_folder_path = os.path.join(user_profile, 'Downloads')
    destination_folder_path = os.path.join(user_profile, 'Music', 'Canciones', 'Otros')
    cover_art_path = os.path.join(user_profile, 'Pictures', 'Imagenes', 'Varias', 'Others.png')
    
    # Arguments
    parser = argparse.ArgumentParser(
        description="This script moves the mp3s on your downloads folder to you music folders' loosies subfolder. " \
        "It also removes some of its metadata in the process and finally sends the processed files to your phone."
    )
    parser.add_argument("-v", '--verbose', action="store_true", help="Specifies extra print output for debug purposes.")
    args = parser.parse_args()

    # Logging set-up according to arguments
    logger = logging.getLogger(__name__)
    if args.verbose:
        logging_level = logging.DEBUG
        logging.basicConfig(level=logging_level)

    # MP3 Changer
    list_of_mp3s = glob.glob(rf'{downloads_folder_path}\*.mp3')
    mp3_transformer = MP3Transformer(list_of_mp3s, logging_level)
    mp3_transformer.change_attributes(cover_art_path)
    
    # Move files to folder locally and to phone
    new_file_paths = move_files(list_of_mp3s, destination_folder_path)
    air_droid = AirDroid(logging_level)
    air_droid.send_to_phone(new_file_paths)
