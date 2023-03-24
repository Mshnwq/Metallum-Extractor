from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys

app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle('Hello world')
window.setGeometry(100, 100, 640, 480)
window.show()
sys.exit(app.exec_())
