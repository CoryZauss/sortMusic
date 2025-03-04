import os
import shutil
import shutil
from mutagen.mp3 import MP3
from mutagen.easyid3  import EasyID3
from mutagen.flac import FLAC

from identify_song import identify
# path=input('enter path to music folder: ')

#! temp paths ~ make user inmput path or select from GUI 
root  = r"E:\\test_sort"
output = r"E:\\test_sorted"

extensions = ("mp3", "wav", "flac", "ogg", "aac", "m4a")
        
# Walk through directories manually
for dirpath, _, filenames in os.walk(root):
    for filename in filenames:

        if filename.lower().endswith(extensions): 
            file_path = os.path.join(dirpath, filename) #! full file path 
            try:
                print(f"Current File: {filename}")
                
                identified = identify(file_path)
                print(f'***** SONG ID: {identified} *****')

                if identified.get('status') == 'success':
                    # TODO: need to check if song already exists before copying
                     
                    result = identified.get('result', {})
                    title = result.get("title", "Unknown Title")
                    artist = result.get("artist", "Unknown Artist")
                    album = result.get("album", "Unknown Album")
                    release_date = result.get("release_date", "")
                    label = result.get("label", "")
                    timecode = result.get("timecode", "")
                    trackNumber = result.get("trackNumber", "")
                    
                    track_name = f"{artist} - {title}"
                    
                    updatedFile = os.path.join(output)  # Base output folder
                    if artist:
                        updatedFile = os.path.join(updatedFile, artist)  # Create artist folder
                    if album:
                        updatedFile = os.path.join(updatedFile, album)  # Create album folder

                    os.makedirs(updatedFile, exist_ok=True)  # Create directories if they don't exist

                    file_extension = os.path.splitext(filename)[1]

                    new_file_path = os.path.join(updatedFile, f"{track_name}{file_extension}")  # Define the full path including the filename and extension
                    
                    shutil.copy(file_path, new_file_path) # copy to new file
                    
                    if file_extension == ".flac" or file_extension == ".wav":
                        modified = FLAC(updatedFile)
                    else:
                        modified = EasyID3(updatedFile)

                    modified["title"] = title
                    modified["artist"] = artist
                    modified["album"] =  album
                    modified["release_date"] = release_date
                    modified["label"] = label
                    modified["timecode"] = timecode

                    os.rename(updatedFile, track_name)
                    modified.save()
                    print(f"SAVED: {track_name} to {output}")
                    
                    #? for now output to new folder
                    #? future: modify in place
                   
                else:
                    print(f"Metadata identification failed for: {filename}")
                    #! try to guess from either meta data or leave alone ?
                    # audio = MP3(file_path, ID3=ID3)
                    # artist = audio.get('TPE1', 'Unknown Artist')
                    # title = audio.get('TPE2', 'Unknown Title')
                    # print(artist, title)
                    new_file_path = os.path.join(output, filename)
                    
                    shutil.copy(file_path, new_file_path)
    
        
            except Exception as e:
                print(f"ERROR: {e}")
                print(f"Dictionary contents: {identified.result}")

    ""
    {'status': 'success', 
     'result': {
         'artist': 'Radiohead', 
         'title': 'Creep', 
         'album': 'Now!...Anglo Anthems', 
         'release_date': '2012-03-13', 
         'label': '(C) 2012 EMI Music México, S.A. de C.V.', 
         'timecode': '03:51', 
         'song_link': 'https://lis.tn/YastwG'
         }}
    
    ""






