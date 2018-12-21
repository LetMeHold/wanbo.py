# -*- coding: utf-8 -*-

from gl import *
from wrap import MainWindow
from PyQt5.QtWidgets import QApplication

app = QApplication(sys.argv)
window = MainWindow()
#window.show()
window.showMaximized()
sys.exit(app.exec_())

