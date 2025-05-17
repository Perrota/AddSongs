# What does it do and why
This program moves all the .mp3 files from a default folder (usually your downloads folder) to a specified folder while changing its attributes to generic tags. Upon doing that, it will prompt you for your Android FTP server configs to send a copy of those files to your phone.

I use it as a way to organize all the singles and loosies I download and instantly copy them to my phone. Most of the songs I download are not from an album so it saves me a lot of time in the long run. Using the same attributes and cover art means they show up under the same album, labeled 'Others'.
# How to use
Run the main.py file. You'll need to have the python interpreter installed for it to work.

For the FTP server part of the program to work, you will need an app like WiFi FTP Server installed on your Android.

The program only has one optional argument: Type '-v' (or '--verbose') if you want the console to print out information about the execution of the script.
# System
This branch of the project should be cross platfom, but it was only tested on Windows 11.

The libraries used include glob, argparse, time, mutagen, pathlib, pyautogui, datetime and logging.