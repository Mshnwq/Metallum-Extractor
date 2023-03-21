from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from window import Ui_MainWindow
from mettalum import Metallum_Worker
from excel import Excel_Worker
from youtube import Youtube_Worker
from folder import Folder_Worker
from functools import partial
import json
import urllib.request
import time, sys, importlib, os, platform, ctypes

fileDirectory = os.path.dirname(__file__)
# import all UI
package = 'UI'
__ui__ = dict()
# for file_name in os.listdir(f"{fileDirectory}\\{package}"):
#     if file_name.endswith('.py') and file_name.startswith('Ui_') and file_name != '__init__.py':
#         module_name = file_name[:-3]
#         # print(f"{module_name[3:]}")
#         __ui__[module_name[3:]] = importlib.import_module(
#             f"{package}.{module_name}", '.')
        
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.band_dict = {
  "band_name": "Nostalghia",        
  "band_pic_link": "https://www.metal-archives.com/images/3/5/4/0/3540472562_logo.jpg?1915",
  "band_albums": [
    {
      "name": "Obsequies for Lost Memories",
      "type": "Full-length",        
      "year": "2020",
      "album_pic_link": "https://www.metal-archives.com/images/8/7/2/2/872201.jpg?1512"
    },
    {
      "name": "Lifeless",
      "type": "Full-length",        
      "year": "2021",
      "album_pic_link": "https://www.metal-archives.com/images/9/2/7/0/927038.jpg?3602"
    },
    {
      "name": "Here, at the End of All Things",
      "type": "Full-length",        
      "year": "2021",
      "album_pic_link": "https://www.metal-archives.com/images/9/9/2/5/992527.jpg?4616"
    },
    {
      "name": "Abandon",
      "type": "Single",
      "year": "2022",
      "album_pic_link": "https://www.metal-archives.com/images/1/0/1/3/1013834.jpg?3722"
    },
    {
      "name": "Olvido",
      "type": "Full-length",        
      "year": "2022",
      "album_pic_link": "https://www.metal-archives.com/images/1/0/2/3/1023834.jpg?1844"
    },
    {
      "name": "Elegy",
      "type": "Single",
      "year": "2022",
      "album_pic_link": "https://www.metal-archives.com/images/1/0/4/6/1046973.jpg?0321"
    },
    {
      "name": "Au milieu de l'hiver",
      "type": "Full-length",        
      "year": "2022",
      "album_pic_link": "https://www.metal-archives.com/images/1/0/5/1/1051820.jpg?2209"
    },
    {
      "name": "R\u00eaverie",       
      "type": "Single",
      "year": "2022",
      "album_pic_link": "https://www.metal-archives.com/images/1/0/6/6/1066365.jpg?2515"
    },
    {
      "name": "Wounds",
      "type": "Full-length",        
      "year": "2022",
      "album_pic_link": "https://www.metal-archives.com/images/1/0/7/9/1079618.jpg?1755"
    }
  ]
}

        self.setWindowIcon(QIcon(":SCFS"))
        if platform.system() == 'Windows':
            myappid = 'mycompany.myproduct.subproduct.version' # arbitrary string
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        elif platform.system() == 'Linux':
            ...
        else:
            print(f"Taskbar Icon not supported in {platform.system()} OS")

        self.setWindowTitle("My Metallum")

        # initialize the ui
        self.init_ui()
    
    def init_ui(self):

        # Window Setup
        self.ui = Ui_MainWindow()
        self.ui.setup_ui(self)
        self.show()

        ''' Button Events '''
        self.ui.extract_event_signal.connect(
                            partial(self.handle_extract_event))
        self.ui.youtube_event_signal.connect(
                            partial(self.handle_youtube_event))
        self.ui.folder_event_signal .connect(
                            partial(self.handle_folder_event))
        self.ui.excel_event_signal  .connect(
                            partial(self.handle_excel_event))

    def handle_extract_event(self):
        data = [['Obsequies for Lost Memories', 'Full-length', '2020'], ['Lifeless', 'Full-length', '2021'], ['Here, at the End of All Things', 'Full-length', 
'2021'], ['Abandon', 'Single', '2022'], ['Olvido', 'Full-length', '2022'], ['Elegy', 'Single', '2022'], ["Au milieu de l'hiver", 'Full-length', 
'2022'], ['Rêverie', 'Single', '2022'], ['Wounds', 'Full-length', '2022']]
        self.ui.update_table(data)
        return
        _query = self.ui.search_input.text()
        if _query == '':
            return
        # create worker and connect slots
        metallum_worker = Metallum_Worker(_query)
        metallum_worker.done_json_signal.connect(
                            partial(self.on_extract_finish, metallum_worker))
        metallum_worker.start()
        ...

    def on_extract_finish(self, worker, band_dict):
        worker.terminate()
        albums = self.store_info(band_dict)
        # print(albums)
        self.ui.update_table(albums)
        self.ui.statusbar.showMessage('extract work finished')
        ...

    def store_info(self, band_dict: dict) -> list:
        self.band_dict = band_dict
        print(json.dumps(band_dict, indent=4))
        self.band_name = band_dict['band_name']
        self.band_pic_link = band_dict['band_pic_link']
        self.all_albums_list = []
        all_albums = band_dict['band_albums']
        for album in all_albums:
            self.all_albums_list.append([album['name'], album['type'], album['year']])
        return self.all_albums_list
        ...

    def handle_excel_event(self):
        excel_worker = Excel_Worker()
        ...

    def on_excel_finish(self, worker):
        worker.terminate()
        self.ui.statusbar.showMessage('excel work finished')
        ...

    def handle_youtube_event(self):
        youtube_worker = Youtube_Worker()
        ...

    def on_youtube_finish(self, worker):
        worker.terminate()
        self.ui.statusbar.showMessage('youtube work finished')
        ...

    def handle_folder_event(self):
        # get the selected albums to save and filter them
        _selected = self.filter_albums(self.ui.get_table_selected())
        # Use QFileDialog to prompt the user for a directory
        _directory = QFileDialog.getExistingDirectory(self, 'Choose Directory')
        if _directory is None:
            return
        # create worker and connect slots
        folder_worker = Folder_Worker(_directory, _selected)
        folder_worker.done_signal.connect(
                            partial(self.on_folder_finish, folder_worker))
        folder_worker.start()
        ...
    
    def on_folder_finish(self, worker):
        worker.terminate()
        self.ui.statusbar.showMessage('folder work finished')
        ...

    def filter_albums(self, album_list) -> dict:
        filtered_dict = dict(self.band_dict)
        filtered_albums = []
        for album in filtered_dict["band_albums"]:
            if [album["name"], album["type"], album["year"]] in album_list:
                filtered_albums.append(album)
        filtered_dict["band_albums"] = filtered_albums
        return filtered_dict


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()
