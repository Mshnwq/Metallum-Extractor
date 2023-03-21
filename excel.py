from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import time, sys, importlib

class Excel_Worker(QThread):
    '''Excel Worker Thread'''
    def __init__(self):
        super().__init__()

    def run(self):
        ...

def main():
    app = QApplication(sys.argv)
    excel_worker = Excel_Worker()
    ...

if __name__ == '__main__':
    main()

