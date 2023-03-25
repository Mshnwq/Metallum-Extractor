import os
import re
import urllib.request

from PyQt5.QtCore import QThread, pyqtSignal


class Folder_Worker(QThread):
    '''Folder Worker Thread'''
    done_signal = pyqtSignal()

    def __init__(self, directory, selected):
        super().__init__()
        self.directory = directory
        self.selected = selected

    def run(self):
        # Create the band directory
        band_name = self.selected["band_name"]
        band_dir = os.path.join(self.directory, band_name)
        os.makedirs(band_dir, exist_ok=True)

        try:
            # Download the band image with a user agent header
            band_pic_link = self.selected["band_pic_link"]
            req = urllib.request.Request(band_pic_link, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as response, open(os.path.join(band_dir, f"{band_name} logo.jpg"), "wb") as outfile:
                outfile.write(response.read())
        
        except Exception as e:
            print(e)

        # Create a directory for each album
        for album in self.selected["band_albums"]:
            album_name = album["name"]
            album_type = album["type"]
            album_year = album["year"]
            if album_type == 'Full-length':
                album_dir = os.path.join(band_dir, 
                            f'{self.sanitize_filename(album_name)} ({album_year})')
            else:
                album_dir = os.path.join(band_dir, 
                            f'{self.sanitize_filename(album_name)} [{album_type}] ({album_year})')
            os.makedirs(album_dir, exist_ok=True)

            try:
                # Download the album cover with a user agent header
                album_pic_link = album["album_pic_link"]
                if album_pic_link != '':
                    req = urllib.request.Request(album_pic_link, headers={'User-Agent': 'Mozilla/5.0'})
                    with urllib.request.urlopen(req) as response, open(os.path.join(album_dir, f"{album_name} cover.jpg"), "wb") as outfile:
                        outfile.write(response.read())
            
            except Exception as e:
                print(e)
        
        self.done_signal.emit()
        ...

    def sanitize_filename(self, name):
        # Remove any characters that can't be used in Windows folder names
        sanitized_name = re.sub(r'[<>:/\\"|?*]', '&', name)
        return sanitized_name

def main():
    ...

if __name__ == '__main__':
    main()

