from gl import *
from ui import *
from wrap.business import Business
from PyQt5.QtWidgets import QMainWindow,QTableWidgetItem,QMenu,QAction,QMessageBox,QFileDialog
from PyQt5.QtCore import QDate,Qt
from PyQt5.QtGui import QIcon,QCursor

class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.setupUi(self)
        GL.LOG = getLogger('WanboLoger', 'logs', 'console.log')
        self.bus = Business()
        self.init()
        GL.LOG.info('主界面启动')

    def closeEvent(self, event):
        if self.bus != None:
            del self.bus
        GL.LOG.info('主界面关闭')

    def init(self):
        self.twQuery.setContextMenuPolicy(Qt.CustomContextMenu)
        self.twQuery.customContextMenuRequested.connect(self.tablePopMenu)
        self.twQuery.horizontalHeader().setStyleSheet("QHeaderView::section{background:skyblue;}")
        self.twQuery.verticalHeader().setStyleSheet("QHeaderView::section{background:skyblue;}")

        self.cmbTable.addItem('无')
        self.cmbTable.addItems(list(self.bus.tables().keys()))
        #self.cmbTable.selectIndex = 0

        self.actFilter = QAction(self)
        self.actFilter.setText('筛选')
        self.popmenu = QMenu(self)
        self.popmenu.addAction(self.actFilter)
        self.actFilter.triggered.connect(self.actFilterClicked)
        
        self.cmbTable.currentIndexChanged.connect(self.cmbTableSelected)
        self.btnRefresh.clicked.connect(self.btnRefreshClicked)
        self.edtFilter.textChanged.connect(self.edtFilterChanged)
        self.btnAdd.clicked.connect(self.btnAddClicked)
        self.twQuery.itemChanged.connect(self.dataItemChanged)

    def dataItemChanged(self, it):
        r = it.row()
        c = it.column()
        id_it = self.twQuery.item(r, 0)
        id_enHead = self.tableQueryHead[0][0]
        id_value = int(id_it.text())
        enHead = self.tableQueryHead[0][c]
        tp = self.tableQueryHead[2][c]
        sql = 'update %s set %s = %TBD where %s = %d' 
        value = it.text()
        if value.strip() == '':
            sql = sql.replace('%TBD','%s', 1)
            value = 'NULL'
        elif tp == 'int':
            sql = sql.replace('%TBD','%d', 1)
            value = int(value)
        elif tp == 'double':
            sql = sql.replace('%TBD','%.2f', 1)
            value = float(value)
        else:
            sql = sql.replace('%TBD','"%s"', 1)
        sql = sql % (self.tableQuery,enHead,value,id_enHead,id_value)
        self.bus.execSql(sql)

    def tablePopMenu(self, pos):
        self.popmenu.popup(QCursor.pos())

    def actFilterClicked(self):
        item = self.twQuery.currentItem()
        self.edtFilter.setText(item.text())

    def fillTableQuery(self, table):
        self.tableQuery = table
        self.tableQueryData = self.bus.selectTableData(self.tableQuery)
        self.tableQueryHead = self.bus.selectTableHead(self.tableQuery)
        self.twQuery.itemChanged.disconnect()
        self.fillTable(self.twQuery, self.tableQuery, self.tableQueryData, self.tableQueryHead)
        self.twQuery.itemChanged.connect(self.dataItemChanged)

    def cmbTableSelected(self, index):
        key = self.cmbTable.itemText(index)
        if key in self.bus.tables():
            self.fillTableQuery(self.bus.tables()[key])

    def btnRefreshClicked(self):
        key = self.cmbTable.currentText()
        if key in self.bus.tables():
            self.fillTableQuery(self.bus.tables()[key])

    def edtFilterChanged(self, txt):
        if len(txt) < 2:
            return
        current = self.twQuery.currentItem()
        items = self.twQuery.findItems(txt, Qt.MatchContains)
        showRows = []
        for it in items:
            if it.row() not in showRows:
                showRows.append(it.row())
        self.twQuery.setVisible(False)
        for i in range(0,self.twQuery.rowCount()):
            if i not in showRows:
                self.twQuery.setRowHidden(i, True)
            else:
                self.twQuery.setRowHidden(i, False)
        self.twQuery.setCurrentItem(current)
        self.twQuery.setVisible(True)

    def fillTable(self, tw, table, data, head):
        tw.clear()
        tw.setColumnCount(len(head[1]))
        tw.setRowCount(len(data))
        tw.setHorizontalHeaderLabels(head[1])
        self.btnAdd.setText('新增')

        tw.setVisible(False)
        for r in range(0,tw.rowCount()):
            for c in range(0,tw.columnCount()):
                tmp = data[r][head[0][c]]
                if tmp == None:
                    tmp = ''
                it = QTableWidgetItem(str(tmp))
                tw.setItem(r,c,it)
                if c == 0:
                    it.setFlags(it.flags() & ~Qt.ItemIsEditable)
                tw.setRowHidden(r, False)
        tw.setVisible(True)

    def btnAddClicked(self):
        key = self.cmbTable.currentText()
        if key not in self.bus.tables():
            return
        if self.btnAdd.text() == '新增':
            self.twQuery.clearContents()
            self.twQuery.setRowCount(1)
            self.btnAdd.setText('确认新增')
        else:
            sql = self.bus.insertTemplates()[key]
            r = 0
            datas = []
            for c in range(1,self.twQuery.columnCount()):
                it = self.twQuery.item(r, c)
                txt = None
                #表格为空或都是空格就以None处理
                if it != None:
                    txt = it.text()
                    if txt.strip() == '':
                        txt = None
                #根据DB中的类型对txt进行处理
                if txt != None:
                    if self.tableQueryHead[2][c] == 'int':
                        sql = sql.replace('%TBD','%d', 1)
                        txt = int(txt)
                    elif self.tableQueryHead[2][c] == 'double':
                        sql = sql.replace('%TBD','%.2f', 1)
                        txt = float(txt)
                    else:
                        sql = sql.replace('%TBD','"%s"', 1)
                else:
                    txt = 'NULL'
                    sql = sql.replace('%TBD','%s', 1)
                datas.append(txt)
            sql = sql % tuple(datas)
            self.bus.execSql(sql)
            self.btnAdd.setText('新增')
            self.btnRefreshClicked()

