# -*- coding: utf-8 -*-

from gl import *
from ui import *
from wrap.business import *
from PyQt5.QtWidgets import QMainWindow,QDialog,QTableWidgetItem,QAbstractItemView,QListWidgetItem,QMenu,QAction,QMessageBox,QFileDialog,QMessageBox,QInputDialog,QTreeWidgetItem,QFileDialog,QShortcut
from PyQt5.QtCore import QDate,Qt
from PyQt5.QtGui import QIcon,QCursor,QBrush,QFont,QKeySequence

class JobDialog(QDialog, Ui_JobDialog):
    def __init__(self, parent=None, bus=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)

        self.bus = bus

        #操作(Job)页面的表格
        self.twJob.setContextMenuPolicy(Qt.CustomContextMenu)
        self.twJob.customContextMenuRequested.connect(self.tableJobMenu)
        self.twJob.horizontalHeader().setStyleSheet("QHeaderView::section{background:skyblue;}")
        self.twJob.verticalHeader().setStyleSheet("QHeaderView::section{background:skyblue;}")
        self.twJob.itemDoubleClicked.connect(self.tableJobItemEdit)

        #操作(Job)页面的右键菜单
        self.menuTableJob = QMenu(self)

        self.actJobRelate = QAction('确认关联', self)
        self.menuTableJob.addAction(self.actJobRelate)
        self.actJobRelate.triggered.connect(self.actJobRelateClicked)

        self.btnJobRefresh.clicked.connect(self.btnJobRefreshClicked)
        self.edtFilterJob.textChanged.connect(self.edtFilterJobChanged)

        self.tableJob = None
        self.tableJobZh = None
        self.tableJobData = None
        self.tableJobHead = None

        self.tableDst = None
        self.twDst = None
        self.twDstHead = None
        self.itemDst = None
        self.txtDst = None

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
            if self.bus.updateTableById(self.tableJob, enHead, tp, new, id_enHead, id_value):
                item.setText(new)
                GL.LOG.info('编辑表格(%s), id(%d)的(%s)由(%s)改为(%s).' % (self.tableJob,id_value,zhHead,old,new))
            else:
                QMessageBox.critical(self, 'Error', '失败！')

    def tableJobMenu(self, pos):
        self.actJobRelate.setVisible(False)
        if self.tableJobZh=='应收账款' or self.tableJobZh=='收支明细':
            self.actJobRelate.setVisible(True)
        self.menuTableJob.popup(QCursor.pos())

    def resetTabJob(self):
        self.twJob.clear()
        self.edtFilterJob.clear()
        self.tableDst = None
        self.twDst = None
        self.twDstHead = None
        self.itemDst = None
        self.txtDst = None

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
        r = item.row()
        c = 1   #关联就是修改明细表的第二列
        id_it = self.twDst.item(r, 0)
        id_enHead = self.tableDstHead[0][0]
        id_value = int(id_it.text())
        enHead = self.tableDstHead[0][c]
        zhHead = self.tableDstHead[1][c]
        tp = self.tableDstHead[2][c]
        old = self.itemDst.text()
        if self.bus.updateTableById(self.tableDst, enHead, tp, self.txtDst, id_enHead, id_value):
            GL.LOG.info('编辑表格(%s), id(%d)的(%s)由(%s)改为(%s).' % (self.tableDst,id_value,zhHead,old,self.txtDst))
            self.itemDst.setText(self.txtDst)
            self.twDst.setCurrentItem(self.itemDst)
        else:
            QMessageBox.critical(self, 'Error', '失败！')

        self.tableDst = None
        self.twDst = None
        self.twDstHead = None
        self.itemDst = None
        self.txtDst = None

    def fillTableJob(self, table):
        self.tableJob = self.bus.tables()[table]
        self.tableJobZh = table
        self.tableJobData = self.bus.selectTableData(self.tableJob)
        self.tableJobHead = self.bus.selectTableHead(self.tableJob)
        self.fillTable(self.twJob, self.tableJob, self.tableJobData, self.tableJobHead)

    def btnJobRefreshClicked(self):
        self.fillTableJob(self.tableJobZh)

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

        tw.setVisible(False)
        for r in range(0,tw.rowCount()):
            for c in range(0,tw.columnCount()):
                tmp = data[r][head[0][c]]
                if tmp == None:
                    tmp = ''
                it = QTableWidgetItem(str(tmp))
                tw.setItem(r,c,it)
                it.setFlags(it.flags() & ~Qt.ItemIsEditable)
                tw.setRowHidden(r, False)
        tw.setVisible(True)

