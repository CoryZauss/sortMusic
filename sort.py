import ctypes, sys
import os
import shutil
from mutagen.mp3 import MP3
from mutagen.easyid3  import EasyID3
from mutagen.flac import FLAC
from identify_song import identify

#! temp paths ~ make user inmput path or select from GUI 
root  = r"E:\\test_sort"
output = r"E:\\test_sorted"

def sort(root, output):

    # root = input('enter path to music folder: ')


    extensions = ("mp3", "wav", "flac", "ogg", "aac", "m4a")
            
    # Walk through directories manually
    for dirpath, _, filenames in os.walk(root):
        for filename in filenames:

            if filename.lower().endswith(extensions): 
                file_path = os.path.join(dirpath, filename) #! full file path 
                try:
                    print()
                    print(f"Current File: {filename}")
                    
                    identified = identify(file_path)
                    
                    if identified is None:
                        print(f"Metadata identification failed for: {filename}")
                        #! try to guess from either meta data or leave alone ?
                        # audio = MP3(file_path, ID3=ID3)
                        # artist = audio.get('TPE1', 'Unknown Artist')
                        # title = audio.get('TPE2', 'Unknown Title')
                        # print(artist, title)
                        new_file_path = os.path.join(output, filename)
                        shutil.copy(file_path, new_file_path)

                    elif identified.get('status') == 'success':
                        # TODO: need to check if song already exists before copying
                        
                        result = identified.get('result', {})
                        title = result.get("title", "Unknown Title")
                        artist = result.get("artist", "Unknown Artist")
                        album = result.get("album", "Unknown Album")
                        label = result.get("label", "")
                        trackNumber = result.get("trackNumber", "")
                        
                        track_name = f"{artist} - {title}"
                        
                        updatedFile = os.path.join(output)  # Base output folder

                        if artist:
                            updatedFile = os.path.join(updatedFile, artist)  # Create artist folder
                        if album:
                            updatedFile = os.path.join(updatedFile, album)  # Create album folder

                        os.makedirs(updatedFile, exist_ok=True)  # Create directories if they don't exist
                        file_extension = os.path.splitext(filename)[1] # get ext
                        new_file_path = os.path.join(updatedFile, f"{track_name}{file_extension}")  # Define the full path including the filename and extension
                        
                        shutil.copy(file_path, new_file_path) # copy to new file
                        print(f"Copy Complete: {new_file_path}")
                        
                        if file_extension == ".flac" or file_extension == ".wav":
                            modified = FLAC(new_file_path)
                        else:
                            modified = EasyID3(new_file_path)
                        
                        modified["title"] = title if title else "Unknown Title"
                        modified["artist"] = artist if artist else "Unknown Artist"
                        modified["album"] = album if album else "Unknown Album"
                        modified["label"] = label if label else ""
                        modified["trackNumber"] = trackNumber if trackNumber else ""
                        modified.save()
                        print(f"SAVED: {track_name} to {output}")
                        
                        #? for now output to new folder
                        #? future: modify in place
        
        
                except Exception as e:
                    print(f"ERROR: {e}")
                    if identified is not None:
                        print(f"Dictionary contents: {identified.get('result')}")
                    else:
                        print(f"No metadata found for the {filename}.")
                    print()


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if is_admin():
    sort(root, output)
else:
    # Re-run the program with admin rights
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)




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






