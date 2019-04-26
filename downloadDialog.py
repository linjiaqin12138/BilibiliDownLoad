# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'DownloadDialog.ui'
#
# Created by: PyQt5 UI code generator 5.12
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_DownLoading(object):
    def setupUi(self, DownLoading):
        DownLoading.setObjectName("DownLoading")
        DownLoading.resize(397, 232)
        self.label = QtWidgets.QLabel(DownLoading)
        self.label.setGeometry(QtCore.QRect(30, 40, 111, 16))
        self.label.setObjectName("label")
        self.label_title = QtWidgets.QLabel(DownLoading)
        self.label_title.setGeometry(QtCore.QRect(30, 70, 321, 31))
        self.label_title.setText("")
        self.label_title.setObjectName("label_title")
        self.progressBar = QtWidgets.QProgressBar(DownLoading)
        self.progressBar.setGeometry(QtCore.QRect(30, 130, 331, 23))
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")
        self.label_v = QtWidgets.QLabel(DownLoading)
        self.label_v.setGeometry(QtCore.QRect(300, 170, 67, 17))
        self.label_v.setObjectName("label_2")
        self.label_p = QtWidgets.QLabel(DownLoading)
        self.label_p.setGeometry(QtCore.QRect(40, 170, 67, 17))
        self.label_p.setObjectName("label_3")

        self.retranslateUi(DownLoading)
        QtCore.QMetaObject.connectSlotsByName(DownLoading)

    def retranslateUi(self, DownLoading):
        _translate = QtCore.QCoreApplication.translate
        DownLoading.setWindowTitle(_translate("DownLoading", "Dialog"))
        self.label.setText(_translate("DownLoading", "正在下载："))
        self.label_v.setText(_translate("DownLoading", "51kb/s"))
        self.label_v.setText(_translate("DownLoading", "24/100M"))


