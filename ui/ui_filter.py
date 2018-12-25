# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/filter.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_FilterDialog(object):
    def setupUi(self, FilterDialog):
        FilterDialog.setObjectName("FilterDialog")
        FilterDialog.resize(765, 446)
        self.verticalLayout = QtWidgets.QVBoxLayout(FilterDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.cmbField = QtWidgets.QComboBox(FilterDialog)
        self.cmbField.setMinimumSize(QtCore.QSize(150, 25))
        self.cmbField.setObjectName("cmbField")
        self.horizontalLayout.addWidget(self.cmbField)
        self.btnAddField = QtWidgets.QPushButton(FilterDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnAddField.sizePolicy().hasHeightForWidth())
        self.btnAddField.setSizePolicy(sizePolicy)
        self.btnAddField.setMinimumSize(QtCore.QSize(0, 25))
        self.btnAddField.setObjectName("btnAddField")
        self.horizontalLayout.addWidget(self.btnAddField)
        self.cbNotIn = QtWidgets.QCheckBox(FilterDialog)
        self.cbNotIn.setMinimumSize(QtCore.QSize(0, 25))
        self.cbNotIn.setObjectName("cbNotIn")
        self.horizontalLayout.addWidget(self.cbNotIn)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.label = QtWidgets.QLabel(FilterDialog)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.rbYear = QtWidgets.QRadioButton(FilterDialog)
        self.rbYear.setObjectName("rbYear")
        self.horizontalLayout.addWidget(self.rbYear)
        self.rbMonth = QtWidgets.QRadioButton(FilterDialog)
        self.rbMonth.setObjectName("rbMonth")
        self.horizontalLayout.addWidget(self.rbMonth)
        self.rbDay = QtWidgets.QRadioButton(FilterDialog)
        self.rbDay.setObjectName("rbDay")
        self.horizontalLayout.addWidget(self.rbDay)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.twFilter = QtWidgets.QTableWidget(FilterDialog)
        self.twFilter.setObjectName("twFilter")
        self.twFilter.setColumnCount(0)
        self.twFilter.setRowCount(0)
        self.verticalLayout.addWidget(self.twFilter)

        self.retranslateUi(FilterDialog)
        QtCore.QMetaObject.connectSlotsByName(FilterDialog)

    def retranslateUi(self, FilterDialog):
        _translate = QtCore.QCoreApplication.translate
        FilterDialog.setWindowTitle(_translate("FilterDialog", "高级筛选"))
        self.btnAddField.setText(_translate("FilterDialog", "添加"))
        self.cbNotIn.setText(_translate("FilterDialog", "不包含"))
        self.label.setText(_translate("FilterDialog", "日期匹配："))
        self.rbYear.setText(_translate("FilterDialog", "年"))
        self.rbMonth.setText(_translate("FilterDialog", "月"))
        self.rbDay.setText(_translate("FilterDialog", "日"))

