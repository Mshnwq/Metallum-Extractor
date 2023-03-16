from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import time, sys, importlib

class Folder_Worker(QThread):
    '''Folder Worker Thread'''
    def __init__(self):
        super().__init__()

    def run(self):
        ...

def main():
    app = QApplication(sys.argv)
    folder_worker = Folder_Worker()
    ...

if __name__ == '__main__':
    main()

