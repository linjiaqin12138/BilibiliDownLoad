# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'DownloadDialog.ui'
#
# Created by: PyQt5 UI code generator 5.12
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(388, 168)
        self.layoutWidget = QtWidgets.QWidget(Dialog)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 20, 368, 132))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.lbDownLoading = QtWidgets.QLabel(self.layoutWidget)
        self.lbDownLoading.setObjectName("lbDownLoading")
        self.verticalLayout.addWidget(self.lbDownLoading)
        spacerItem = QtWidgets.QSpacerItem(366, 13, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lbCur = QtWidgets.QLabel(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbCur.sizePolicy().hasHeightForWidth())
        self.lbCur.setSizePolicy(sizePolicy)
        self.lbCur.setMinimumSize(QtCore.QSize(0, 30))
        self.lbCur.setObjectName("lbCur")
        self.horizontalLayout.addWidget(self.lbCur)
        self.verticalLayout.addLayout(self.horizontalLayout)
        spacerItem1 = QtWidgets.QSpacerItem(366, 13, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.Progress = QtWidgets.QProgressBar(self.layoutWidget)
        self.Progress.setEnabled(True)
        self.Progress.setProperty("value", 24)
        self.Progress.setObjectName("Progress")
        self.verticalLayout.addWidget(self.Progress)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.lbDownLoading.setText(_translate("Dialog", "下载中："))
        self.lbCur.setText(_translate("Dialog", "当前下载："))


