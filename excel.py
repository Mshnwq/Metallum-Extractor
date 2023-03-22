import logging
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import time, sys, importlib, openpyxl

class Excel_Worker(QThread):
    '''Excel Worker Thread'''
    done_signal = pyqtSignal()

    def __init__(self, file_name, selected):
        super().__init__()
        self.file_name = file_name
        self.selected = selected

    def run(self):
        try:
            # Load the Excel file
            workbook  = openpyxl.load_workbook(self.file_name)
            # Select the active worksheet
            worksheet = workbook.active 
            
            # Write init row
            row = ['', self.selected['band_name'], '']
            # Write album data
            for album in self.selected["band_albums"]:
                    row.append(album["name"])
            
            # Append the new band row to the worksheet
            worksheet.append(row)
            # Save workbook
            workbook.save(self.file_name)
        except Exception as e:
                logging.error(e)

        self.done_signal.emit()
        ...

def main():
    app = QApplication(sys.argv)
    excel_worker = Excel_Worker()
    ...

if __name__ == '__main__':
    main()

