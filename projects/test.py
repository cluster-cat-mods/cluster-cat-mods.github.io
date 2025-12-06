from pathlib import Path
from mutagen.mp3 import MP3
from mutagen.flac import FLAC
from mutagen.id3 import ID3
import os
import json

def file_read(filename):
    with open(filename, "r") as f:
        temp = json.load(f)
    return temp

def file_write(filename, data):
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

def lijst(filename):
    temp = file_read(filename)
    for entry in temp:
        for key in entry:
            print(key, ":", entry[key])
        print("==================") 

def toevoegen(filename, data):
    temp = file_read(filename)
    temp.append(data)
    file_write(filename, temp)

def read_metadata(file_path):
    ext = file_path.suffix.lower()
    
    try:
        if ext == ".mp3":
            audio = MP3(file_path, ID3=ID3)
            tags = audio.tags
        elif ext == ".flac":
            audio = FLAC(file_path)
            tags = audio.tags
            print(f"Available tags for {file_path}: {tags}")  # Print available tags for FLAC files
        else:
            print(f"Unsupported file type: {ext}")
            return

        # Extract common metadata and handle cases where tags may not exist
        title = tags.get("TIT2") or tags.get("title")
        artist = tags.get("TPE1") or tags.get("artist")
        album = tags.get("TALB") or tags.get("album")

        # Check if the tag is a list or not
        title = title[0] if isinstance(title, list) and title else 'Unknown'
        artist = artist[0] if isinstance(artist, list) and artist else 'Unknown'
        album = album[0] if isinstance(album, list) and album else 'Unknown'

        # Prepare data for JSON serialization
        data = {
            "filepath": str(file_path),  # Include the full file path as a string
            "title": title,
            "album": album,
            "artist": artist
        }
        print(data)
        toevoegen("./HTML/test.json", data)
    except Exception as e:
        print(f"Error reading tags for {file_path}: {e}")




# Function to process all music files in a folder and its subfolders
def process_folder(folder_path):
    folder = Path(folder_path)
    file_write("./HTML/test.json", [])  # Initialize test.json with an empty list

    if not folder.is_dir():
        print(f"{folder_path} is not a valid folder.")
        return

    # Use rglob to find all audio files in the folder and subfolders
    for file_path in folder.rglob("*.mp3"):
        print(f"Processing {file_path}")  # Debug statement
        read_metadata(file_path)

    for file_path in folder.rglob("*.flac"):
        print(f"Processing {file_path}")  # Debug statement
        read_metadata(file_path)

# Specify the folder path
folder_path = "./HTML/media/music"

# Process all files in the folder and its subfolders
process_folder(folder_path)
