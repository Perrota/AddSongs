import logging
from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3, APIC, PictureType # type: ignore
import os

class MP3Transformer():

    def __init__(self, list_of_mp3s, logger_level = 0):
        self.list_of_mp3s = list_of_mp3s
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logger_level)

    def change_attributes(self, cover_art_path: str):

        self.logger.info(f"Attempting to change attributes of {len(self.list_of_mp3s)} file(s).")
        for mp3f in self.list_of_mp3s:

            self.logger.info(f"Changing text attributes of file {os.path.basename(mp3f)}.")
            mp3File = MP3(mp3f, ID3=EasyID3)
            mp3File['album'] = 'Otros'
            mp3File['albumartist'] = 'Otros'
            mp3File['genre'] = 'Other'
            
            self.remove_attribute(mp3File, 'date')
            self.remove_attribute(mp3File, 'tracknumber')

            self.logger.info("Saving file.")
            mp3File.save()

            # # Change cover art
            audio = MP3(mp3f, ID3=ID3)
            
            # Add new
            self.logger.info("Deleting old cover art.")
            if audio.tags is not None:
                audio.tags.delall("APIC")
            self.logger.info("Adding new cover art.")
            with open(cover_art_path, "rb") as art:
                apic = APIC(data=art.read(), type=PictureType.COVER_FRONT, desc='Cover', mime="img/jpeg")
                audio['APIC:'] = apic

            audio.save()
    
    def remove_attribute(self, mp3, attribute_name):
        self.logger.info(f"Attempting to remove {attribute_name}.")
        try:
            mp3.pop(attribute_name)
        except Exception as e:
            self.logger.error(e)
            self.logger.info(f"Failed to remove {attribute_name}.")