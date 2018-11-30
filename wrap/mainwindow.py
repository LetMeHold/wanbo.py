from gl import *
from ui import *
from wrap.business import Business
from PyQt5.QtWidgets import QMainWindow,QTableWidgetItem,QMenu,QAction,QMessageBox,QFileDialog
from PyQt5.QtCore import QDate,Qt

class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.setupUi(self)
        GL.LOG = getLogger('WanboLoger', 'logs', 'console.log')
        self.bus = Business()
        self.relate()
        self.inittable()
        GL.LOG.info('主界面启动')
        self.edt.setText('test')

    def closeEvent(self, event):
        if self.bus != None:
            del self.bus
        GL.LOG.info('主界面关闭')

    def relate(self):
        self.btnQuery.clicked.connect(self.getTableData)

    def inittable(self):
        self.twData.setContextMenuPolicy(Qt.CustomContextMenu)
        #self.twData.customContextMenuRequested.connect(self.tablePopMenu)
        self.twData.horizontalHeader().setStyleSheet("QHeaderView::section{background:skyblue;}")
        self.twData.verticalHeader().setStyleSheet("QHeaderView::section{background:skyblue;}")
        #self.actdel = QAction(self)
        #self.actdel.setText('删除')
        #self.popmenu = QMenu(self)
        #self.popmenu.addAction(self.actdel)
        #self.actdel.triggered.connect(self.actionDel)

    def getTableData(self):
        table = self.edt.text()
        ret = self.bus.selectTableData(table)
        (enHead,zhHead) = self.bus.selectTableHead(table)
        self.twData.clear()
        self.twData.setColumnCount(len(enHead))
        self.twData.setRowCount(len(ret))
        self.twData.setHorizontalHeaderLabels(zhHead)
        self.twData.setVisible(False)
        self.filldata = []
        for r in range(0,self.twData.rowCount()):
            for c in range(0,self.twData.columnCount()):
                tmp = ret[r][enHead[c]]
                if tmp == None:
                    tmp = ''
                it = QTableWidgetItem(str(tmp))
                self.twData.setItem(r,c,it)
            #self.filldata.append(tmp)
        self.twData.setVisible(True)


