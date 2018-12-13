from gl import *
from ui import *
from wrap.business import Business
from PyQt5.QtWidgets import QMainWindow,QTableWidgetItem,QMenu,QAction,QMessageBox,QFileDialog,QMessageBox,QInputDialog,QTreeWidgetItem
from PyQt5.QtCore import QDate,Qt
from PyQt5.QtGui import QIcon,QCursor,QBrush

class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.setupUi(self)
        GL.LOG = getLogger('WanboLoger', 'logs', 'console.log')
        GL.LOG.info('主程序启动')
        self.bus = Business()
        self.init()

    def closeEvent(self, event):
        if self.bus != None:
            del self.bus
        GL.LOG.info('主程序关闭')

    def actQryTestClicked(self):
        #self.statusbar.showMessage('hhh', 5000)
        #QMessageBox.critical(self, '失败', '大大的失败')
        #sql = self.bus.getInsertTemplates(self.tableQuery, self.tableQueryHead[0])
        #GL.LOG.info(sql)
        #ret = self.bus.getContractAmount('year(date) = 2018')
        #ret = self.bus.getContractAmount('合同总额')
        ret = self.bus.getBalanceStats()
        print(ret)
        pass


    def init(self):
        #数据管理(Query)页面的表格
        self.twQuery.setContextMenuPolicy(Qt.CustomContextMenu)
        self.twQuery.customContextMenuRequested.connect(self.tableQueryMenu)
        self.twQuery.horizontalHeader().setStyleSheet("QHeaderView::section{background:skyblue;}")
        self.twQuery.verticalHeader().setStyleSheet("QHeaderView::section{background:skyblue;}")
        self.twQuery.itemDoubleClicked.connect(self.tableQueryItemEdit)

        self.trQuery.setColumnCount(1)
        self.trQuery.setHeaderHidden(True)
        t = QTreeWidgetItem(self.trQuery, ['表格管理',])
        for k,v in self.bus.tables().items():
            QTreeWidgetItem(t, [k,])
        self.trQuery.expandAll()
        self.trQuery.currentItemChanged.connect(self.treeQueryItemActivated)
        self.trQuery.sortItems(0, Qt.AscendingOrder)

        #统计汇总(stats)页面的表格
        self.twStats.setContextMenuPolicy(Qt.CustomContextMenu)
        #self.twStats.customContextMenuRequested.connect(self.tableStatsMenu)
        self.twStats.horizontalHeader().setStyleSheet("QHeaderView::section{background:skyblue;}")
        self.twStats.verticalHeader().setStyleSheet("QHeaderView::section{background:skyblue;}")
        #self.twStats.itemDoubleClicked.connect(self.tableStatsItemEdit)

        self.trStats.setColumnCount(1)
        self.trStats.setHeaderHidden(True)
        t = QTreeWidgetItem(self.trStats, ['统计汇总',])
        for k in self.bus.stats():
            QTreeWidgetItem(t, [k,])
        self.trStats.expandAll()
        self.trStats.currentItemChanged.connect(self.treeStatsItemActivated)
        self.trStats.sortItems(0, Qt.AscendingOrder)

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

        #其他控件关联
        self.btnRefresh.clicked.connect(self.btnRefreshClicked)
        self.btnJobRefresh.clicked.connect(self.btnJobRefreshClicked)
        self.btnAdd.clicked.connect(self.btnAddClicked)
        self.btnJobClose.clicked.connect(self.btnJobCloseClicked)
        self.edtFilter.textChanged.connect(self.edtFilterChanged)
        self.edtFilterJob.textChanged.connect(self.edtFilterJobChanged)

        #更多需要初始化的内容
        self.jobTabIndex = 2
        self.tab.removeTab(self.jobTabIndex)   #默认隐藏job标签页
        self.tableQuery = None
        self.tableQueryZh = None
        self.tableQueryData = None
        self.tableQueryHead = None
        self.tableJob = None
        self.tableJobZh = None
        self.tableJobData = None
        self.tableJobHead = None
        self.tableDst = None
        self.twDst = None
        self.twDstHead = None
        self.itemDst = None
        self.txtDst = None

    def treeQueryItemActivated(self, itemNew, itemOld):
        self.fillTableQuery(itemNew.text(0))

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
            item.setText(new)
            GL.LOG.info('编辑表格(%s), id(%d)的(%s)由(%s)改为(%s).' % (self.tableQuery,id_value,zhHead,old,new))
            self.bus.updateTableById(self.tableQuery, enHead, tp, new, id_enHead, id_value)

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
            item.setText(new)
            GL.LOG.info('编辑表格(%s), id(%d)的(%s)由(%s)改为(%s).' % (self.tableJob,id_value,zhHead,old,new))
            self.bus.updateTableById(self.tableJob, enHead, tp, new, id_enHead, id_value)

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
        self.resetTabJob()
        table_zh = '应收账款'
        self.tab.insertTab(self.jobTabIndex, self.tabJob, '操作-%s'%table_zh)
        self.tab.setCurrentIndex(index)
        self.fillTableJob(table_zh)
        self.edtFilterJob.setText(item.text())

        self.tableDst = self.tableQuery
        self.twDst = self.twQuery
        self.tableDstHead = self.tableQueryHead
        self.itemDst = self.twQuery.item(item.row(), 1)
        self.txtDst = None

    def actQryRelateDetailClicked(self):
        item = self.twQuery.currentItem()
        if item == None:
            return
        self.resetTabJob()
        table_zh = '收支明细'
        index = 1
        self.tab.insertTab(index, self.tabJob, '操作-%s'%table_zh)
        self.tab.setCurrentIndex(index)
        self.fillTableJob(table_zh)
        self.edtFilterJob.setText(item.text())
        #操作页加载后才能取到tableJob的各项数据
        self.tableDst = self.tableJob
        self.twDst = self.twJob
        self.tableDstHead = self.tableJobHead
        self.itemDst = None
        self.txtDst = self.twQuery.item(item.row(),0).text()

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
        self.itemDst.setText(self.txtDst)
        GL.LOG.info(self.tableJob)
        GL.LOG.info('编辑表格(%s), id(%d)的(%s)由(%s)改为(%s).' % (self.tableDst,id_value,zhHead,old,self.txtDst))
        self.bus.updateTableById(self.tableDst, enHead, tp, self.txtDst, id_enHead, id_value)
        self.twDst.setCurrentItem(self.itemDst)

        self.tableDst = None
        self.twDst = None
        self.twDstHead = None
        self.itemDst = None
        self.txtDst = None

    def fillTableQuery(self, table):
        if table not in self.bus.tables():
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

    #def cmbTableSelected(self, index):
        #self.fillTableQuery()

    def btnRefreshClicked(self):
        self.fillTableQuery(self.tableQueryZh)

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
        if self.tableQueryZh not in self.bus.tables():
            return
        if self.btnAdd.text() == '新增':
            self.twQuery.clearContents()
            self.twQuery.setRowCount(1)
            self.btnAdd.setText('确认新增')
        else:
            datas = []
            r = 0
            for c in range(0,self.twQuery.columnCount()):
                it = self.twQuery.item(r, c)
                txt = None
                #表格为空或都是空格就以None处理
                if it != None:
                    txt = it.text()
                    if txt.strip() == '':
                        txt = 'NULL'
                else:
                    txt = 'NULL'
                datas.append(txt)
            self.bus.insertTable(self.tableQueryZh, datas)
            self.btnAdd.setText('新增')
            self.btnRefreshClicked()

    def treeStatsItemActivated(self, itemNew, itemOld):
        if itemNew.text(0) == '应收账款统计':
            tw = self.twStats
            tw.clear()
            tw.setColumnCount(7)
            tw.setRowCount(13)
            ret = self.bus.getAccountStats()
            ret['今年合同欠款率'] = ret['今年未收款额'] / ret['今年合同额']
            ret['历年合同欠款率'] = ret['历年未收款额'] / ret['历年合同额']
            ret['总欠款率'] = ret['未收款总额'] / ret['合同总额']
            struct = self.bus.statsAccount()
            for k,v in ret.items():
                if k not in struct:
                    continue
                if v == None:
                    v = 0.0
                it1 = QTableWidgetItem(str(k))
                it1.setFlags(it1.flags() & ~Qt.ItemIsEditable)
                it1.setBackground(QBrush(Qt.lightGray))
                if struct[k]['form'] == '百分比':
                    it2 = QTableWidgetItem('%.2f%%' % (v*100))
                else:
                    it2 = QTableWidgetItem(str(v))
                it2.setFlags(it2.flags() & ~Qt.ItemIsEditable)
                row = struct[k]['row']
                col = struct[k]['column']
                tw.setItem(row, col, it1)
                tw.setItem(row+1, col, it2)
        elif itemNew.text(0) == '开票统计':
            tw = self.twStats
            tw.clear()
            heads = self.bus.statsInvoice()
            ret = self.bus.getInvoiceStats()
            tw.setColumnCount(len(heads))
            tw.setRowCount(len(ret))
            tw.setHorizontalHeaderLabels(heads)
            row = 0
            for tmp in ret:
                for k,v in tmp.items():
                    if v == None:
                        v = 0.0
                    col = heads.index(k)
                    it = QTableWidgetItem(str(v))
                    it.setFlags(it.flags() & ~Qt.ItemIsEditable)
                    tw.setItem(row, col, it)
                it = QTableWidgetItem(str(v))
                it.setFlags(it.flags() & ~Qt.ItemIsEditable)
                tw.setItem(row, col, it)
                row += 1
        elif itemNew.text(0) == '收支统计':
            tw = self.twStats
            tw.clear()
            heads = self.bus.statsBalance()
            ret = self.bus.getBalanceStats()
            tw.setColumnCount(len(heads))
            tw.setRowCount(len(ret))
            tw.setHorizontalHeaderLabels(heads)
            row = 0
            for k1,v1 in ret.items():
                it = QTableWidgetItem(str(k1))
                it.setFlags(it.flags() & ~Qt.ItemIsEditable)
                col = 0
                tw.setItem(row, col, it)
                for k2,v2 in v1.items():
                    it = QTableWidgetItem(str(v2))
                    it.setFlags(it.flags() & ~Qt.ItemIsEditable)
                    col = heads.index(k2) + 1
                    tw.setItem(row, col, it)
                row += 1
        elif itemNew.text(0) == '费用统计':
            tw = self.twStats
            tw.clear()
            heads = self.bus.statsCost()
            ret = self.bus.getCostStats()
            tw.setColumnCount(len(heads))
            tw.setRowCount(100)
            tw.setHorizontalHeaderLabels(heads)
            row = 0
            for class1,v1 in ret.items():
                it = QTableWidgetItem(str(class1))
                it.setFlags(it.flags() & ~Qt.ItemIsEditable)
                col = 0
                tw.setItem(row, col, it)
                row += 1
                for class2,v2 in v1.items():
                    GL.LOG.info(row)
                    #if row >= 1:
                        #GL.LOG.info('ret')
                        #return
                    it = QTableWidgetItem(str(class2))
                    it.setFlags(it.flags() & ~Qt.ItemIsEditable)
                    col = 1
                    tw.setItem(row, col, it)
                    for v3 in v2:
                        mon = v3['月份']
                        cost = v3['费用']
                        if cost == None:
                            cost = 0.0
                        it = QTableWidgetItem(str(cost))
                        it.setFlags(it.flags() & ~Qt.ItemIsEditable)
                        col = heads.index(mon)
                        tw.setItem(row, col, it)
                    row += 1
                    GL.LOG.info(row)
        else:
            pass


