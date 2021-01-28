#!/bin/python
# Google text to speech
# Use 'gtts-cli --all' to see all supported languages
import os
import sys
import time
import platform
import datetime
# Google text to speech API 'pip install gtts'
from gtts import gTTS

#---------------------------------------------------------------------
# Debug = 1 or 0
#---------------------------------------------------------------------
debug = 1
curr_lang = 'en-us'
#---------------------------------------------------------------------
# File extensions to use for the IVR audio conversion, update as needed.
#---------------------------------------------------------------------
file_exts = ('.txt','.text')

#=================================================================================================================
# NOTES
# Tested on macOS Big Sur, Windows 10 and Windows Server 2016
# On macOS you may see the message “sox” or "ffmpeg" cannot be opened because the developer cannot be verified
# To fix:  Click Cancel or OK on newer versions of MacOS
# 1. Open up System Preferences
# 2. Go to Security and Privacy -> General
# 3. There will be a message about the program that was blocked, with the option to Open Anyway
#=================================================================================================================

#---------------------------------------------------------------------
# Formatted date string to use in the filename 
#---------------------------------------------------------------------
date_string = datetime.datetime.now().strftime("%Y-%m-%d_%H.%M.%S")

#---------------------------------------------------------------------
# Get the current operating system (Windows, Linux or Darwin) and path
#---------------------------------------------------------------------
curr_os = platform.system()
curr_dir = os.path.dirname(os.path.realpath(__file__)) + "/"

#---------------------------------------------------------------------
# Use appropriate binary for the operating system
#---------------------------------------------------------------------
if (curr_os == 'Darwin'):
    sox = curr_dir + "sox-14.4.2/sox"
    if debug : print("Current OS: ", curr_os)
else:
    sox = curr_dir + "Convert/sox.exe"

if debug : print('Current path: ',curr_dir)

dirs = os.listdir(curr_dir)
#---------------------------------------------------------------------
# Loop over [curr_dir] and grab files that end in the [file_exts] var
#---------------------------------------------------------------------
for filename in dirs:
    if filename.endswith(file_exts):
        curr_file = os.path.splitext(curr_dir + filename)[0] + '_' + date_string
        if debug : print('Processing ',curr_file)
     
        #---------------------------------------------------------------------
        # Remove temp wav file and clear the file_text var
        #--------------------------------------------------------------------- 
        file_text = ''
        if os.path.exists(curr_dir + 'temp.wav') : os.remove(curr_dir + 'temp.wav')
        if os.path.exists(curr_dir + 'temp.mp3') : os.remove(curr_dir + 'temp.mp3')

        #---------------------------------------------------------------------
        # Remove temp wav file and clear the file_text var
        #---------------------------------------------------------------------
        file_open = open(filename, 'r')
        file_text = file_open.read()
        file_open.close
        
        #---------------------------------------------------------------------
        # Convert the text from the prompt file above to an mp3 file using gTTs
        #---------------------------------------------------------------------
        tts = gTTS(text=file_text, lang=curr_lang, slow=False)
        tts.save(curr_dir + 'temp.mp3')
        time.sleep(4)

        if debug : print('The file temp.mp3 was created')
        
        #---------------------------------------------------------------------
        # Convert the MP3 file to a temp WAV format using ffmpeg
        #---------------------------------------------------------------------
        convert_mp3_to_wav = curr_dir + 'sox-14.4.2/ffmpeg -i ' + curr_dir + 'temp.mp3 ' + curr_dir + 'temp.wav'
        o = os.popen(convert_mp3_to_wav).read()
        print(o)
        
        #---------------------------------------------------------------------
        # Convert the WAV temp file to U-Law format for North American IVR systems
        #---------------------------------------------------------------------
        sox_args = "--bits 8 --rate 8000 --channels 1 --encoding u-law --show-progress"
        convert_wav_to_ulaw = '"' + sox + '"' + ' "' + curr_dir + 'temp.wav" ' + sox_args + ' "' + curr_file + '.wav"'
        print(convert_wav_to_ulaw)
        o = os.popen(convert_wav_to_ulaw).read()
        print(o)

        #---------------------------------------------------------------------
        # Clean up temp files
        #--------------------------------------------------------------------- 
        #if os.path.exists(curr_dir + 'temp.wav') : os.remove(curr_dir + 'temp.wav')
        #if os.path.exists(curr_dir + 'temp.mp3') : os.remove(curr_dir + 'temp.mp3')

exit(0)
