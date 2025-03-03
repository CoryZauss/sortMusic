import os
import shutil
import glob
import fnmatch
from mutagen.mp3 import MP3
from mutagen.id3 import ID3


# look thru music folder to create plan:
# aka a list of all the paths of all the files
# check each file/ identify song (AUDD ? )
# rename and place in the correct artists folder with correct album and meta data 

# path=input('enter path to music folder: ')

#! temp paths ~ make user inmput path or select from GUI 
root  = r"E:\\test_sort"
output = r"E:\\test_sorted"

extensions = ("mp3", "wav", "flac", "ogg", "aac", "m4a")
        
# Walk through directories manually
for dirpath, _, filenames in os.walk(root):
    for filename in filenames:
        if filename.lower().endswith(extensions):  # Case insensitive check
            
            #! here is the full file path of the audio file
            file_path = os.path.join(dirpath, filename)
            
            try:
                print(f"Current File: {filename}")

                audio = MP3(file_path, ID3=ID3)
                artist = audio.get('TPE1', 'Unknown Artist')
                title = audio.get('TPE2', 'Unknown Title')
                print(artist, title)

                #? IF THINGS ARE UNKNOWN FIND FINGERPRINT 
                #? maybe just find fingerprint anyway
                #?  If no print, can we guess thru the files name ?
            
            except Exception as e:
                print(f"ERROR: {e}")




