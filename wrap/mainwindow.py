from gl import *
from ui import *
from wrap.business import Business
from PyQt5.QtWidgets import QMainWindow,QTableWidgetItem,QMenu,QAction,QMessageBox,QFileDialog,QMessageBox,QInputDialog
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
        #数据管理(Query)页面的表格
        self.twQuery.setContextMenuPolicy(Qt.CustomContextMenu)
        self.twQuery.customContextMenuRequested.connect(self.tableQueryMenu)
        self.twQuery.horizontalHeader().setStyleSheet("QHeaderView::section{background:skyblue;}")
        self.twQuery.verticalHeader().setStyleSheet("QHeaderView::section{background:skyblue;}")
        self.twQuery.itemDoubleClicked.connect(self.tableQueryItemEdit)

        #操作(Job)页面的表格
        self.twJob.setContextMenuPolicy(Qt.CustomContextMenu)
        self.twJob.customContextMenuRequested.connect(self.tableJobMenu)
        self.twJob.horizontalHeader().setStyleSheet("QHeaderView::section{background:skyblue;}")
        self.twJob.verticalHeader().setStyleSheet("QHeaderView::section{background:skyblue;}")
        self.twJob.itemDoubleClicked.connect(self.tableJobItemEdit)

        #数据管理(Query)页面的右键菜单
        self.menuTableQuery = QMenu(self)

        self.actQryFilter = QAction(self)
        self.actQryFilter.setText('筛选')
        self.menuTableQuery.addAction(self.actQryFilter)
        self.actQryFilter.triggered.connect(self.actQryFilterClicked)

        self.actQryRelateAccount = QAction(self)
        self.actQryRelateAccount.setText('关联账款')
        self.menuTableQuery.addAction(self.actQryRelateAccount)
        self.actQryRelateAccount.triggered.connect(self.actQryRelateAccountClicked)

        self.actQryRelateDetail = QAction(self)
        self.actQryRelateDetail.setText('关联明细')
        self.menuTableQuery.addAction(self.actQryRelateDetail)
        self.actQryRelateDetail.triggered.connect(self.actQryRelateDetailClicked)

        self.actQryTest = QAction(self)
        self.actQryTest.setText('测试')
        self.menuTableQuery.addAction(self.actQryTest)
        self.actQryTest.triggered.connect(self.actQryTestClicked)

        #操作(Job)页面的右键菜单
        self.menuTableJob = QMenu(self)

        self.actJobRelate = QAction(self)
        self.actJobRelate.setText('确认关联')
        self.menuTableJob.addAction(self.actJobRelate)
        self.actJobRelate.triggered.connect(self.actJobRelateClicked)

        #其他控件初始化
        self.cmbTable.addItem('无')
        self.cmbTable.addItems(list(self.bus.tables().keys()))
        #self.cmbTable.selectIndex = 0

        #其他控件关联
        self.cmbTable.currentIndexChanged.connect(self.cmbTableSelected)
        self.btnRefresh.clicked.connect(self.btnRefreshClicked)
        self.btnJobRefresh.clicked.connect(self.btnJobRefreshClicked)
        self.btnAdd.clicked.connect(self.btnAddClicked)
        self.btnJobClose.clicked.connect(self.btnJobCloseClicked)
        self.edtFilter.textChanged.connect(self.edtFilterChanged)
        self.edtFilterJob.textChanged.connect(self.edtFilterJobChanged)

        #更多需要初始化的内容
        self.tab.removeTab(1)   #默认隐藏job标签页

    def tableQueryItemEdit(self, item):
        r = item.row()
        c = item.column()
        if c == 0:
            self.statusbar.showMessage('编号不可修改！', 5000)
            return
        old = item.text()
        (new, ok) = QInputDialog.getText(self,'编辑表格','输入新内容：', text=old)
        if ok and new!=old:
            id_it = self.twQuery.item(r, 0)
            id_enHead = self.tableQueryHead[0][0]
            id_value = int(id_it.text())
            enHead = self.tableQueryHead[0][c]
            zhHead = self.tableQueryHead[1][c]
            tp = self.tableQueryHead[2][c]
            sql = 'update %s set %s = %TBD where %s = %d' 
            GL.LOG.info('编辑表格(%s), id(%d)的(%s)由(%s)改为(%s).' % (self.tableQuery,id_value,zhHead,old,new))
            item.setText(new)
            if new.strip() == '':
                sql = sql.replace('%TBD','%s', 1)
                new = 'NULL'
            elif tp == 'int':
                sql = sql.replace('%TBD','%d', 1)
                new = int(new)
            elif tp == 'double':
                sql = sql.replace('%TBD','%.2f', 1)
                new = float(new)
            else:
                sql = sql.replace('%TBD','"%s"', 1)
            sql = sql % (self.tableQuery,enHead,new,id_enHead,id_value)
            self.bus.execSql(sql)

    def tableJobItemEdit(self, item):
        r = item.row()
        c = item.column()
        if c == 0:
            self.statusbar.showMessage('编号不可修改！', 5000)
            return
        old = item.text()
        (new, ok) = QInputDialog.getText(self,'编辑表格','输入新内容：', text=old)
        if ok and new!=old:
            id_it = self.twJob.item(r, 0)
            id_enHead = self.tableJobHead[0][0]
            id_value = int(id_it.text())
            enHead = self.tableJobHead[0][c]
            zhHead = self.tableJobHead[1][c]
            tp = self.tableJobHead[2][c]
            sql = 'update %s set %s = %TBD where %s = %d' 
            GL.LOG.info('编辑表格(%s), id(%d)的(%s)由(%s)改为(%s).' % (self.tableJob,id_value,zhHead,old,new))
            item.setText(new)
            if new.strip() == '':
                sql = sql.replace('%TBD','%s', 1)
                new = 'NULL'
            elif tp == 'int':
                sql = sql.replace('%TBD','%d', 1)
                new = int(new)
            elif tp == 'double':
                sql = sql.replace('%TBD','%.2f', 1)
                new = float(new)
            else:
                sql = sql.replace('%TBD','"%s"', 1)
            sql = sql % (self.tableJob,enHead,new,id_enHead,id_value)
            self.bus.execSql(sql)

    def btnJobCloseClicked(self):
        self.resetTabJob()

    def tableQueryMenu(self, pos):
        self.actQryRelateAccount.setVisible(False)
        self.actQryRelateDetail.setVisible(False)
        if self.twQuery.currentItem() != None:
            self.actQryFilter.setVisible(True)
            if self.tableQueryZh == '应收账款':
                self.actQryRelateDetail.setVisible(True)
            elif self.tableQueryZh == '收支明细':
                self.actQryRelateAccount.setVisible(True)
        self.menuTableQuery.popup(QCursor.pos())

    def tableJobMenu(self, pos):
        self.actJobRelate.setVisible(False)
        if self.tableJobZh=='应收账款' or self.tableJobZh=='收支明细':
            self.actJobRelate.setVisible(True)
        self.menuTableJob.popup(QCursor.pos())

    def actQryFilterClicked(self):
        item = self.twQuery.currentItem()
        if item == None:
            return
        self.edtFilter.setText(item.text())

    def resetTabJob(self):
        self.twJob.clear()
        self.edtFilterJob.clear()
        self.tab.removeTab(1)

    def actQryRelateAccountClicked(self):
        item = self.twQuery.currentItem()
        if item == None:
            return
        self.twDst = self.twQuery
        self.itemDst = self.twQuery.item(item.row(), 1)
        self.txtDst = None
        self.resetTabJob()
        table_zh = '应收账款'
        index = 1
        self.tab.insertTab(index, self.tabJob, '操作-%s'%table_zh)
        self.tab.setCurrentIndex(index)
        self.fillTableJob(table_zh)
        self.edtFilterJob.setText(item.text())

    def actQryRelateDetailClicked(self):
        item = self.twQuery.currentItem()
        if item == None:
            return
        self.twDst = self.twJob
        self.itemDst = None
        self.txtDst = self.twQuery.item(item.row(),0).text()
        self.resetTabJob()
        table_zh = '收支明细'
        index = 1
        self.tab.insertTab(index, self.tabJob, '操作-%s'%table_zh)
        self.tab.setCurrentIndex(index)
        self.fillTableJob(table_zh)
        self.edtFilterJob.setText(item.text())

    def actJobRelateClicked(self):
        item = self.twJob.currentItem()
        if item == None:
            return
        if self.itemDst!=None and self.txtDst==None:
            self.txtDst = self.twJob.item(item.row(),0).text()
        elif self.itemDst==None and self.txtDst!=None:
            self.itemDst = self.twJob.item(item.row(),1)
        else:
            QMessageBox.critical(self, 'Error', '关联时数据有误, 请重试！')
            return
        self.itemDst.setText(self.txtDst)
        self.twDst.setCurrentItem(self.itemDst)
        self.twDst = None
        self.itemDst = None
        self.txtDst = None

    def actQryTestClicked(self):
        #self.statusbar.showMessage('hhh', 5000)
        #QMessageBox.critical(self, '失败', '大大的失败')
        pass

    def fillTableQuery(self, table=None):
        if table == None:
            table = self.cmbTable.currentText()
            if table not in self.bus.tables():
                print(table)
                return
        self.tableQuery = self.bus.tables()[table]
        self.tableQueryZh = table
        self.tableQueryData = self.bus.selectTableData(self.tableQuery)
        self.tableQueryHead = self.bus.selectTableHead(self.tableQuery)
        self.fillTable(self.twQuery, self.tableQuery, self.tableQueryData, self.tableQueryHead)

    def fillTableJob(self, table):
        self.tableJob = self.bus.tables()[table]
        self.tableJobZh = table
        self.tableJobData = self.bus.selectTableData(self.tableJob)
        self.tableJobHead = self.bus.selectTableHead(self.tableJob)
        self.fillTable(self.twJob, self.tableJob, self.tableJobData, self.tableJobHead)

    def cmbTableSelected(self, index):
        self.fillTableQuery()

    def btnRefreshClicked(self):
        self.fillTableQuery()

    def btnJobRefreshClicked(self):
        self.fillTableJob(self.tableJobZh)

    def edtFilterChanged(self, txt):
        if txt == '':
            for r in range(0,self.twQuery.rowCount()):
                self.twQuery.setRowHidden(r, False)
            return
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

    def edtFilterJobChanged(self, txt):
        if txt == '':
            for r in range(0,self.twJob.rowCount()):
                self.twJob.setRowHidden(r, False)
            return
        if len(txt) < 2:
            return
        current = self.twJob.currentItem()
        items = self.twJob.findItems(txt, Qt.MatchContains)
        showRows = []
        for it in items:
            if it.row() not in showRows:
                showRows.append(it.row())
        self.twJob.setVisible(False)
        for i in range(0,self.twJob.rowCount()):
            if i not in showRows:
                self.twJob.setRowHidden(i, True)
            else:
                self.twJob.setRowHidden(i, False)
        self.twJob.setCurrentItem(current)
        self.twJob.setVisible(True)

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
                #if c == 0:
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

