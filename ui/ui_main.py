# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/main.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")
        self.tabQuery = QtWidgets.QWidget()
        self.tabQuery.setObjectName("tabQuery")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.tabQuery)
        self.verticalLayout_2.setContentsMargins(16, 16, 16, 16)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label_11 = QtWidgets.QLabel(self.tabQuery)
        self.label_11.setMinimumSize(QtCore.QSize(0, 25))
        self.label_11.setObjectName("label_11")
        self.gridLayout.addWidget(self.label_11, 0, 0, 1, 1)
        self.cmbTable = QtWidgets.QComboBox(self.tabQuery)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cmbTable.sizePolicy().hasHeightForWidth())
        self.cmbTable.setSizePolicy(sizePolicy)
        self.cmbTable.setMinimumSize(QtCore.QSize(150, 25))
        self.cmbTable.setObjectName("cmbTable")
        self.gridLayout.addWidget(self.cmbTable, 0, 1, 1, 1)
        self.edtFilter = QtWidgets.QLineEdit(self.tabQuery)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtFilter.sizePolicy().hasHeightForWidth())
        self.edtFilter.setSizePolicy(sizePolicy)
        self.edtFilter.setMinimumSize(QtCore.QSize(200, 25))
        self.edtFilter.setObjectName("edtFilter")
        self.gridLayout.addWidget(self.edtFilter, 1, 1, 1, 1)
        self.btnAdd = QtWidgets.QPushButton(self.tabQuery)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnAdd.sizePolicy().hasHeightForWidth())
        self.btnAdd.setSizePolicy(sizePolicy)
        self.btnAdd.setMinimumSize(QtCore.QSize(0, 50))
        self.btnAdd.setObjectName("btnAdd")
        self.gridLayout.addWidget(self.btnAdd, 0, 4, 2, 1)
        self.label_10 = QtWidgets.QLabel(self.tabQuery)
        self.label_10.setMinimumSize(QtCore.QSize(0, 25))
        self.label_10.setObjectName("label_10")
        self.gridLayout.addWidget(self.label_10, 1, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 3, 1, 1)
        self.btnRefresh = QtWidgets.QPushButton(self.tabQuery)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnRefresh.sizePolicy().hasHeightForWidth())
        self.btnRefresh.setSizePolicy(sizePolicy)
        self.btnRefresh.setMinimumSize(QtCore.QSize(0, 50))
        self.btnRefresh.setObjectName("btnRefresh")
        self.gridLayout.addWidget(self.btnRefresh, 0, 2, 2, 1)
        self.verticalLayout_2.addLayout(self.gridLayout)
        self.twData = QtWidgets.QTableWidget(self.tabQuery)
        self.twData.setObjectName("twData")
        self.twData.setColumnCount(0)
        self.twData.setRowCount(0)
        self.verticalLayout_2.addWidget(self.twData)
        self.tabWidget.addTab(self.tabQuery, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.tabWidget.addTab(self.tab_2, "")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.tabWidget.addTab(self.tab_3, "")
        self.verticalLayout.addWidget(self.tabWidget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_11.setText(_translate("MainWindow", "选择表"))
        self.btnAdd.setText(_translate("MainWindow", "新增"))
        self.label_10.setText(_translate("MainWindow", "筛选"))
        self.btnRefresh.setText(_translate("MainWindow", "刷新"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabQuery), _translate("MainWindow", "数据管理"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "数据统计"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("MainWindow", "页"))

