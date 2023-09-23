import os

# Directory containing the files to rename
directory = '.'

# Iterate through files in the directory
for filename in os.listdir(directory):
    # Split the input string into parts
    if not filename.endswith('.py'):
        parts = filename.split(' - ')
        
        # Extract the track number and title
        album_year = parts[0]
        album_title = ' - '.join([item for item in parts[1:]]).strip()

        # Create the new file name
        new_filename = f"{album_title} ({album_year})"
        # Build the full paths
        old_path = os.path.join(directory, filename)
        new_path = os.path.join(directory, new_filename)
        print(f"Old name: {old_path} -> New Name {new_path}")

        # Rename the file
        os.rename(old_path, new_path)

print("Album renaming complete.")

