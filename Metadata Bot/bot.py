import os
import re
import time
import eyed3

# Function to update metadata for a single MP3 file
def update_mp3_metadata(mp3_file_path, genre, sub_genre, artist, album, year, track_title, track_number, track_total) -> None:
    # Load the MP3 file
    audiofile = eyed3.load(mp3_file_path)

    try:
        # Modify the metadata
        audiofile.tag.album = album
        audiofile.tag.artist = artist
        audiofile.tag.title = track_title
        audiofile.tag.track_num = (int(track_number), int(track_total))  # Track number and total tracks (set total to 0 for now)
        audiofile.tag.genre = f'{genre}; {sub_genre}' #TODO
        audiofile.tag.recording_date = year
        
        # Save the changes
        audiofile.tag.save()
    
    except Exception as e:
        print(e)
        print()

# Function to process a directory recursively
def process_directory(root_dir):
    for dirpath, _, filenames in os.walk(root_dir):
        for index, filename in enumerate(filenames):
            if filename.endswith('.mp3'):
                # Parse the directory structure to get metadata
                parts = dirpath.split(os.path.sep)
                # print(parts)
                genre, sub_genre, artist, album, track = parts[-4], parts[-3], parts[-2], parts[-1], filename[::]
                album_match = re.search(r'\((\d{4})\)', album)
                album_name = album.replace(album_match.group(0), '').strip()
                album_year = album_match.group(1)
                track_total = len(filenames)

                # TODO focus
                # track_info = track.split(' - ')
                # track_number = track_info[0]
                # track_title = ' - '.join([item for item in track_info[1:]]).replace('', '')
                track_number = index+1
                track_title = track.replace('.mp3','').strip()
                # Full path to the MP3 file
                mp3_file_path = os.path.join(dirpath, filename)

                print(f"Genre: {genre}")
                print(f"Sub-Genre: {sub_genre}")
                print(f"Artist: {artist}")
                print(f"Album name: {album_name}")
                print(f"Album year: {album_year}")
                print(f"Track: {track}")
                print(f"Track#: {track_number}")
                print(f"Track title: {track_title}")
                print(f"Total: {track_total}")
                
                # Update metadata
                update_mp3_metadata(mp3_file_path, genre, sub_genre, artist, album_name, album_year, track_title, track_number, track_total)
                time.sleep(0.1)

# Specify the root directory to start processing
root_directory = './Test Bot'

# Call the function to process the directory recursively
process_directory(root_directory)
