from gl import *
from ui import *
from wrap import *
from PyQt5.QtWidgets import QApplication

app = QApplication(sys.argv)
window = MainWindow()
#window.show()
window.showMaximized()
sys.exit(app.exec_())

