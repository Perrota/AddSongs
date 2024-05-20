# What does it do and why
This program moves all the .mp3 files from a default folder (usually your downloads folder) to a specified folder while changing its attributes to generic tags. Upon doing that, it will open airdroid and send a copy of those files to your phone.

I use it as a way to organize all the singles and loosies I download and instantly copy them to my phone. Most of the songs I download are not from an album so it saves me a lot of time in the long run. Using the same attributes and cover art means they show up under the same album, labeled 'Others'.
# How to use
Run the main.py file. You'll need to have the python interpreter installed for it to work.

For the airdroid part of the program to work, you will obviously need to have that program installed on your PC and Android phone. It's also recommended you save your credentials in the app as to save time. The script should be able to recognize when the connection to the phone is made and send the songs you downloaded.

If the script fails to detect when your phone connects (or guesses wrong), you might want to experiment with the 'SymbolToLocate.png' file. This image's job is to find this icon when it appears:

![Phone Icon to locate on screen](image.jpg "Phone Icon")

The program only has one optional argument: Type '-v' if you want the console to print out information about the execution of the script.
# System
Tested on Windows 11. Should also work on Windows 10. Not sure about older versions of Windows. Will most likely not work on other OS.

The libraries used include glob, sys, time, mutagen, os, pyautogui, datetime and logging