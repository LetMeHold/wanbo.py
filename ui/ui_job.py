# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/job.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_JobDialog(object):
    def setupUi(self, JobDialog):
        JobDialog.setObjectName("JobDialog")
        JobDialog.resize(766, 445)
        self.verticalLayout = QtWidgets.QVBoxLayout(JobDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.label_13 = QtWidgets.QLabel(JobDialog)
        self.label_13.setMinimumSize(QtCore.QSize(0, 25))
        self.label_13.setObjectName("label_13")
        self.horizontalLayout_7.addWidget(self.label_13)
        self.edtFilterJob = QtWidgets.QLineEdit(JobDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtFilterJob.sizePolicy().hasHeightForWidth())
        self.edtFilterJob.setSizePolicy(sizePolicy)
        self.edtFilterJob.setMinimumSize(QtCore.QSize(200, 25))
        self.edtFilterJob.setObjectName("edtFilterJob")
        self.horizontalLayout_7.addWidget(self.edtFilterJob)
        self.btnJobRefresh = QtWidgets.QPushButton(JobDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnJobRefresh.sizePolicy().hasHeightForWidth())
        self.btnJobRefresh.setSizePolicy(sizePolicy)
        self.btnJobRefresh.setMinimumSize(QtCore.QSize(0, 25))
        self.btnJobRefresh.setObjectName("btnJobRefresh")
        self.horizontalLayout_7.addWidget(self.btnJobRefresh)
        spacerItem = QtWidgets.QSpacerItem(747, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout_7)
        self.twJob = QtWidgets.QTableWidget(JobDialog)
        self.twJob.setObjectName("twJob")
        self.twJob.setColumnCount(0)
        self.twJob.setRowCount(0)
        self.verticalLayout.addWidget(self.twJob)

        self.retranslateUi(JobDialog)
        QtCore.QMetaObject.connectSlotsByName(JobDialog)

    def retranslateUi(self, JobDialog):
        _translate = QtCore.QCoreApplication.translate
        JobDialog.setWindowTitle(_translate("JobDialog", "操作"))
        self.label_13.setText(_translate("JobDialog", "筛选"))
        self.btnJobRefresh.setText(_translate("JobDialog", "刷新"))

