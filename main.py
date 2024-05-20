import glob
import sys
import time
from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3, APIC, PictureType
import os
import pyautogui as pya
from datetime import datetime, timedelta
import logging

def change_attributes(mp3s_to_change: list, cover_art_path: str) -> list:

    logger.info(f"Attempting to change attributes of {len(mp3s_to_change)} file(s).")
    for mp3f in mp3s_to_change:

        logger.info(f"Changing text attributes of file {os.path.basename(mp3f)}.")
        mp3File = MP3(mp3f, ID3=EasyID3)
        mp3File['album'] = 'Otros'
        mp3File['albumartist'] = 'Otros'
        mp3File['genre'] = 'Other'
        
        logger.info("Attempting to remove date and tracknumber.")
        try:
            mp3File.pop('date')
        except:
            logger.info("Failed to remove date.")

        try:
            mp3File.pop('tracknumber')
        except:
            logger.info("Failed to remove tracknumber.")
        
        logger.info("Saving file.")
        mp3File.save()

        # # Change cover art
        logger.info("Chaning cover art.")
        audio = ID3(mp3f)

        # Delete old if exists
        PicTag = audio.get("APIC:")
        if PicTag != None:
            logger.info("Existing cover detected. Deleting it...")
            del audio["APIC:"]
        
        # Add new
        logger.info("Adding new.")
        with open(cover_art_path, "rb") as art:
            apic = APIC(data=art.read(), type=PictureType.COVER_FRONT, desc='Cover', mime="img/jpeg")
            audio['APIC:'] = apic

        audio.save()

def move_files(mp3s: list, destination_folder_path: str):

    new_file_paths = []
    logger.info(f"Attempting to move {len(mp3s)} file(s).")
    for mp3f in mp3s:
        new_file_name = os.path.join(destination_folder_path, os.path.basename(mp3f))
        logger.info(f"Moving file to destination: {new_file_name}")
        os.rename(mp3f, new_file_name)
        new_file_paths.append(new_file_name)
        
    return new_file_paths

def open_airdroid():
    pya.press('win', interval=2)
    time.sleep(1)
    pya.typewrite('apps:airdroid', interval=2/10)
    pya.press('enter', interval=2*2)

def wait_for_connection():
    function_start = datetime.now()
    while not type(pya.locateOnScreen(os.path.join(os.path.dirname(__file__), "SymbolToLocate.png"), grayscale=False)) == pya.pyscreeze.Box:
        logger.info("Still waiting.")
        time.sleep(1)
        if datetime.now() > function_start + timedelta(seconds=40):
            logger.info("Connection not stablished.")
            return "timeout"
    logger.info("Connection stablished.")
    return "Ok"

def send_to_phone(files: list):
    
    logger.info(f"There are {len(files)} files to send.")
    if any(files):

        logger.info("Opening airdroid.")
        open_airdroid()
        logger.info("Waiting for connection.")
        connection_status = wait_for_connection()

        if not connection_status == "timeout":

            # Send files
            pya.click(pya.size()[0] * 0.3, pya.size()[1] * 0.4)
            time.sleep(1)
            pya.click(pya.size()[0] * 0.44, pya.size()[1] * 0.66)
            time.sleep(1)
            pya.typewrite('"' + '" "'.join(new_file_paths) + '"')
            logger.info(f"Typed {new_file_paths}.")
            time.sleep(1)
            pya.press('enter')
            logger.info("Done sending.")

        else:
            print(connection_status)

if __name__ == "__main__":

    # Environ default name
    user_profile = os.environ.get("USERPROFILE")

    # Variables
    downloads_folder_path = os.path.join(user_profile, 'Downloads')
    destination_folder_path = os.path.join(user_profile, 'Music', 'Canciones', 'Otros')
    cover_art_path = os.path.join(user_profile, 'Pictures', 'Imagenes', 'Varias', 'Others.png')

    list_of_mp3s = glob.glob(rf'{downloads_folder_path}\*.mp3')
    
    # Logging set-up according to arguments
    logger = logging.getLogger()
    if len(sys.argv) > 1:
        if sys.argv[1] == '-v':
            logging.basicConfig(level=logging.DEBUG)
    
    # Process
    change_attributes(list_of_mp3s, cover_art_path)
    new_file_paths = move_files(list_of_mp3s, destination_folder_path)
    send_to_phone(new_file_paths)
