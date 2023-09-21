import os

# Directory containing the files to rename
root_dir = '.'

# Iterate through files in the directory
for dirpath, _, filenames in os.walk(root_dir):
    for filename in filenames:
        if filename.endswith('.mp3'):
            # Split the input string into parts
            parts = filename.split(' - ')
            
            # Extract the track number and title
            track = parts[0].split('.')
            track_title = ' - '.join([item for item in parts[1:]]).strip()

            # Extract file type
            # meta = parts[-1].split('.')
            # extension = meta[-1]

            # Create the new file name
            # new_filename = f"{track_title}.{extension}"
            new_filename = f"{track_title}"
            # Build the full paths
            old_path = os.path.join(dirpath, filename)
            new_path = os.path.join(dirpath, new_filename)
            print(f"Old name: {old_path} -> New Name {new_path}")

            # Rename the file
            os.rename(old_path, new_path)

print("Tracks renaming complete.")

