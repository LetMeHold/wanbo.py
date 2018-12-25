# -*- coding: utf-8 -*-

from gl import *
from ui import *
from PyQt5.QtWidgets import QMainWindow,QDialog,QTableWidgetItem,QAbstractItemView,QListWidgetItem,QMenu,QAction,QMessageBox,QFileDialog,QMessageBox,QInputDialog,QTreeWidgetItem,QFileDialog
from PyQt5.QtCore import QDate,Qt
from PyQt5.QtGui import QIcon,QCursor,QBrush,QFont

class FilterDialog(QDialog, Ui_FilterDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)

        self.twFilter.setContextMenuPolicy(Qt.CustomContextMenu)
        self.twFilter.customContextMenuRequested.connect(self.twFilterMenu)
        self.twFilter.horizontalHeader().setStyleSheet("QHeaderView::section{background:skyblue;}")
        self.twFilter.verticalHeader().setStyleSheet("QHeaderView::section{background:skyblue;}")
        #self.twFilter.setEditTriggers(QAbstractItemView.NoEditTriggers);
        self.twFilter.itemDoubleClicked.connect(self.tableFilterItemEdit)
        self.twFilter.currentItemChanged.connect(self.tableFilterCurrentItemChanged)
        self.menuTwFilter = QMenu(self)

        self.actDel = QAction(self)
        self.actDel.setText('删除')
        self.menuTwFilter.addAction(self.actDel)
        self.actDel.triggered.connect(self.actDelClicked)
        self.actDelCol = QAction(self)
        self.actDelCol.setText('删除列')
        self.menuTwFilter.addAction(self.actDelCol)
        self.actDelCol.triggered.connect(self.actDelColClicked)
        self.actClear = QAction(self)
        self.actClear.setText('清空')
        self.menuTwFilter.addAction(self.actClear)
        self.actClear.triggered.connect(self.actClearClicked)
        self.actFlush = QAction(self)
        self.actFlush.setText('刷新')
        self.menuTwFilter.addAction(self.actFlush)
        self.actFlush.triggered.connect(self.actFlushClicked)

        self.btnAddField.clicked.connect(self.btnAddFieldClicked)
        self.cbNotIn.stateChanged.connect(self.cbNotInStateChanged)

        self.rbDay.setChecked(True)

        self.zhHead = []
        self.enHead = []
        self.typ = []
        self.data = {}
        self.notin = {}
        self.respond = True
        self.fullHead = None

    def twFilterMenu(self):
        self.menuTwFilter.popup(QCursor.pos())

    def clear(self):
        self.twFilter.clear()
        self.zhHead.clear()
        self.enHead.clear()
        self.typ.clear()
        self.data.clear()
        self.notin.clear()

    def tableFilterCurrentItemChanged(self, new, old):
        if new == None:
            return
        col = new.column()
        it = self.twFilter.horizontalHeaderItem(col)
        self.respond = False
        if it != None:
            if it.text() in self.notin:
                self.cbNotIn.setChecked(True)
            else:
                self.cbNotIn.setChecked(False)
        else:
            self.cbNotIn.setChecked(False)
        self.respond = True

    def cbNotInStateChanged(self, state):
        if self.respond == False:
            return
        it = self.twFilter.currentItem()
        it_h = self.twFilter.horizontalHeaderItem(it.column())
        if it==None or it_h==None:
            return
        if self.cbNotIn.isChecked():
            self.notin[it_h.text()] = True
        else:
            self.notin[it_h.text()] = False

    def add(self, zhHead, value):
        index = self.fullHead[1].index(zhHead)
        enHead = self.fullHead[0][index]
        typ = self.fullHead[2][index]

        if zhHead not in self.zhHead:
            self.zhHead.append(zhHead)
            self.enHead.append(enHead)
            self.typ.append(typ)
            self.data[zhHead] = []

        try:
            if value!=None and value not in self.data[zhHead]:
                if value=='' or value=='空':
                    value = '空'
                elif typ == 'int':
                    value = int(value)
                elif typ == 'double':
                    value = float(value.replace(',',''))
                self.data[zhHead].append(value)
        except:
            err = '内容类型不匹配'
            GL.LOG.error(err)
            QMessageBox.critical(self, 'Error', err)

        self.flushTable()

    def actClearClicked(self):
        self.clear()

    def actFlushClicked(self):
        self.flushTable()

    def actDelClicked(self):
        it = self.twFilter.currentItem()
        if it != None:
            r = it.row()
            c = it.column()
            del self.data[self.zhHead[c]][r]
            if len(self.data[self.zhHead[c]]) == 0:
                self.actDelColClicked()
            else:
                self.flushTable()

    def actDelColClicked(self):
        c = self.twFilter.currentColumn()
        it = self.twFilter.horizontalHeaderItem(c)
        if it != None:
            del self.data[self.zhHead[c]]
            del self.enHead[c]
            del self.typ[c]
            del self.zhHead[c]
            self.flushTable()

    def sql(self):
        if len(self.zhHead) == 0:
            return None
        sql = ''
        for n in range(0, len(self.zhHead)):
            if len(self.data[self.zhHead[n]]) == 0:
                continue
            field = self.enHead[n]
            if self.typ[n]=='date':
                if self.rbMonth.isChecked():
                    field = 'date_format(%s,"%%Y-%%m")' % field
                elif self.rbYear.isChecked():
                    field = 'date_format(%s,"%%Y")' % field
            notin = ''
            orand = 'or'
            if self.zhHead[n] in self.notin and self.notin[self.zhHead[n]]:
                notin = 'not'
                orand = 'and'
            if '空' in self.data[self.zhHead[n]]:
                sql += '(%s is %s null %s %s %s in %s) and ' % (self.enHead[n],notin,orand,field,notin,self.data[self.zhHead[n]])
            else:
                sql += '%s %s in %s and ' % (field,notin,self.data[self.zhHead[n]])
        sql = sql.rstrip(' and ')
        sql = sql.replace('[', '(')
        sql = sql.replace(']', ')')
        #sql = sql.replace(', \'空\'', '')
        #sql = sql.replace('\'空\',', '')
        #sql = sql.replace('\'空\'', '')
        sql = sql.replace('空', '')
        return sql

    def flushTable(self):
        self.twFilter.clear()
        self.twFilter.setColumnCount(20)
        self.twFilter.setRowCount(15)
        #先全部初始化为空是为了能双击出发弹框编辑而不是默认编辑
        for r in range(0,self.twFilter.rowCount()):
            for c in range(0,self.twFilter.columnCount()):
                it = QTableWidgetItem('')
                it.setFlags(it.flags() & ~Qt.ItemIsEditable)
                self.twFilter.setItem(r, c, it)
        self.twFilter.setHorizontalHeaderLabels(self.zhHead)
        for c in range(0, len(self.zhHead)):
            for r in range(0, len(self.data[self.zhHead[c]])):
                value = self.data[self.zhHead[c]][r]
                if self.typ[c]=='double' and value!='空':
                    txt = format(value, ',')
                else:
                    txt = str(value)
                it = QTableWidgetItem(txt)
                it.setFlags(it.flags() & ~Qt.ItemIsEditable)
                self.twFilter.setItem(r, c, it)

    def flushCombobox(self, head):
        self.fullHead = head
        self.cmbField.clear()
        self.cmbField.addItems(head[1])

    def tableFilterItemEdit(self, item):
        if item == None:
            return
        r = item.row()
        c = item.column()
        if c >= len(self.zhHead):
            return
        old = item.text()
        (new, ok) = QInputDialog.getText(self,'编辑表格','输入新内容：', text=old)
        if new == '':
            new = '空'
        if ok and new!=old:
            if r < len(self.data[self.zhHead[c]]):
                del self.data[self.zhHead[c]][r]
            self.add(self.zhHead[c], new)
            self.flushTable()

    def btnAddFieldClicked(self):
        field = self.cmbField.currentText()
        if field not in self.zhHead:
            self.add(field, None)

