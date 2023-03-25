import ctypes
import platform
import sys
from functools import partial

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QFileDialog, QMainWindow, QMessageBox

from excel import Excel_Worker
from folder import Folder_Worker
from mettalum import Metallum_Worker
from window import Ui_MainWindow
from youtube import Youtube_Worker


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.setWindowIcon(QIcon(":SCFS"))
        if platform.system() == 'Windows':
            myappid = 'mycompany.myproduct.subproduct.version'  # arbitrary string
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
                myappid) # type: ignore
        elif platform.system() == 'Linux':
            ...
        else:
            print(f"Taskbar Icon not supported in {platform.system()} OS")

        self.setWindowTitle("My Metallum")

        # initialize the ui
        self.init_ui()

    def init_ui(self) -> None:

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
        
        # disable buttons until extract is done
        self.ui.folder_button.setDisabled(True) 
        self.ui.excel_button.setDisabled(True) 
        self.ui.youtube_button.setDisabled(True) 

    def handle_extract_event(self) -> None:
        # get qeuery
        _query = self.ui.search_input.text()
        if _query == '':
            return None
        # create worker and connect slots
        metallum_worker = Metallum_Worker(_query, 
                    self.ui.album_img_checkbox.isChecked())
        metallum_worker.done_json_signal.connect(
            partial(self.on_extract_finish, metallum_worker))
        metallum_worker.start()
        ...

    def on_extract_finish(self, worker, band_dict) -> None:
        worker.terminate()
        albums = self.store_info(band_dict)
        # print(albums)
        self.ui.update_table(albums)
        # enable action buttons
        self.ui.folder_button.setDisabled(False) 
        self.ui.excel_button.setDisabled(False) 
        self.ui.youtube_button.setDisabled(False) 
        self.ui.statusbar.showMessage('extract work finished')
        ...

    def store_info(self, band_dict: dict) -> list:
        self.band_dict = band_dict
        # print(json.dumps(band_dict, indent=4))
        self.band_name = band_dict['band_name']
        self.band_pic_link = band_dict['band_pic_link']
        self.all_albums_list = []
        all_albums = band_dict['band_albums']
        for album in all_albums:
            self.all_albums_list.append(
                [album['name'], album['type'], album['year']])
        return self.all_albums_list
        ...

    def handle_excel_event(self) -> None:
        # get the selected albums to save and filter them
        table_selected = self.ui.get_table_selected()
        if len(table_selected) == 0:
            self.throw_dialog()
            return None
        _selected = self.filter_albums(table_selected)
        # Use QFileDialog to prompt the user for a excel file
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self,
            "QFileDialog.getOpenFileName()", "",
            "Text Files (*.xlsx);;All Files (*)", options=options)
        if file_name == '':
            return None
        # create worker and connect slots
        excel_worker = Excel_Worker(file_name, _selected)
        excel_worker.done_signal.connect(
            partial(self.on_excel_finish, excel_worker))
        excel_worker.start()
        ...

    def on_excel_finish(self, worker) -> None:
        worker.terminate()
        self.ui.statusbar.showMessage('excel work finished')
        ...

    def handle_youtube_event(self) -> None:
        # get the selected albums to save and filter them
        table_selected = self.ui.get_table_selected()
        if len(table_selected) == 0:
            self.throw_dialog()
            return None
        _selected = self.filter_albums(table_selected)
        # create worker and connect slots
        youtube_worker = Youtube_Worker(_selected)
        youtube_worker.done_signal.connect(
            partial(self.on_excel_finish, youtube_worker))
        youtube_worker.start()
        ...

    def on_youtube_finish(self, worker) -> None:
        worker.terminate()
        self.ui.statusbar.showMessage('youtube work finished')
        ...

    def handle_folder_event(self) -> None:
        # get the selected albums to save and filter them
        table_selected = self.ui.get_table_selected()
        if len(table_selected) == 0:
            self.throw_dialog()
            return None
        _selected = self.filter_albums(table_selected)
        # Use QFileDialog to prompt the user for a directory
        _directory = QFileDialog.getExistingDirectory(self, 'Choose Directory')
        if _directory is None:
            return None
        # create worker and connect slots
        folder_worker = Folder_Worker(_directory, _selected)
        folder_worker.done_signal.connect(
            partial(self.on_folder_finish, folder_worker))
        folder_worker.start()
        ...

    def on_folder_finish(self, worker) -> None:
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
        ...

    def throw_dialog(self) -> None:
        dialog = QMessageBox()
        dialog.setWindowTitle("Error!")
        dialog.setText("Select entires from table")
        dialog.setIcon(QMessageBox.Critical)
        dialog.exec_()
        ...


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()
