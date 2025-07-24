import logging
from pathlib import Path

from mutagen.easyid3 import EasyID3
from mutagen.id3 import APIC, ID3, PictureType  # type: ignore
from mutagen.mp3 import MP3

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.WARNING)

class MP3Transformer():

    def __init__(self, list_of_mp3s: list[Path], logger_level: int = 0) -> None:
        self.list_of_mp3s = list_of_mp3s
        logging.basicConfig(level=logger_level)

    def change_attributes(self, cover_art_path: str) -> None:

        logger.info(f"Attempting to change attributes of {len(self.list_of_mp3s)} file(s).")
        for mp3f in self.list_of_mp3s:

            logger.info(f"Changing text attributes of file {mp3f.name}.")
            mp3File = MP3(str(mp3f), ID3=EasyID3)
            mp3File['album'] = 'Otros'
            mp3File['albumartist'] = 'Otros'
            mp3File['genre'] = 'Other'
            
            self.remove_attribute(mp3File, 'date')
            self.remove_attribute(mp3File, 'tracknumber')

            logger.info("Saving file.")
            mp3File.save()

            # # Change cover art
            audio = MP3(str(mp3f), ID3=ID3)
            
            # Add new
            logger.info("Deleting old cover art.")
            if audio.tags is not None:
                audio.tags.delall("APIC")
            logger.info("Adding new cover art.")
            with open(cover_art_path, "rb") as art:
                apic = APIC(data=art.read(), type=PictureType.COVER_FRONT, desc='Cover', mime="img/jpeg")
                audio['APIC'] = apic

            audio.save()
    
    @staticmethod
    def remove_attribute(mp3: MP3, attribute_name:str) -> None:
        logger.info(f"Attempting to remove {attribute_name}.")
        try:
            mp3.pop(attribute_name)
        except Exception as e:
            logger.error(e)
            logger.info(f"Failed to remove {attribute_name}.")