import logging
import os
import time
from datetime import datetime, timedelta

import pyautogui as pya


class AirDroid():

    def __init__(self, logging_level):
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging_level)
        logging.getLogger('PIL').setLevel(logging.WARNING)
        self.open_airdroid()
        self.connection_status = self.wait_for_connection()

    def open_airdroid(self):
        self.logger.info("Opening airdroid.")
        pya.press('win', interval=2)
        time.sleep(1)
        pya.typewrite('apps:airdroid', interval=2/10)
        pya.press('enter', interval=2*2)

    def wait_for_connection(self) -> str:
        self.logger.info("Waiting for connection.")
        function_start = datetime.now()
        connected_indicator = os.path.join(os.path.dirname(__file__), "SymbolToLocate.png")
        while True:
            try:
                pya.locateOnScreen(connected_indicator, grayscale=False)
                
            except Exception:
                if datetime.now() > function_start + timedelta(seconds=40):
                    self.logger.info("Connection not stablished.")
                    return "timeout"
                else:
                    self.logger.info("Still waiting.")
                    time.sleep(1)
                break

        self.logger.info("Connection stablished.")
        return "Ok"

    def send_to_phone(self, files: list):
        
        self.logger.info(f"There are {len(files)} files to send.")
        if any(files):

            if not self.connection_status == "timeout":

                # Send files
                pya.click(pya.size()[0] * 0.3, pya.size()[1] * 0.4)
                time.sleep(1)
                pya.click(pya.size()[0] * 0.44, pya.size()[1] * 0.66)
                time.sleep(1)
                pya.typewrite('"' + '" "'.join(files) + '"')
                self.logger.info(f"Typed {files}.")
                time.sleep(1)
                pya.press('enter')
                self.logger.info("Done sending.")

            else:
                print(self.connection_status)