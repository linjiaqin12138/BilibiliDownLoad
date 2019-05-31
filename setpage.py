# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'SetPage.ui'
#
# Created by: PyQt5 UI code generator 5.12
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(405, 276)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        self.RadioHigh = QtWidgets.QRadioButton(Dialog)
        self.RadioHigh.setGeometry(QtCore.QRect(20, 100, 117, 22))
        self.RadioHigh.setObjectName("RadioHigh")
        self.RadioLow = QtWidgets.QRadioButton(Dialog)
        self.RadioLow.setGeometry(QtCore.QRect(20, 130, 117, 22))
        font = QtGui.QFont()
        font.setUnderline(False)
        font.setStrikeOut(False)
        self.RadioLow.setFont(font)
        self.RadioLow.setObjectName("RadioLow")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(20, 70, 231, 17))
        self.label_2.setObjectName("label_2")
        self.line = QtWidgets.QFrame(Dialog)
        self.line.setGeometry(QtCore.QRect(20, 50, 361, 20))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.line_2 = QtWidgets.QFrame(Dialog)
        self.line_2.setGeometry(QtCore.QRect(20, 150, 361, 20))
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(20, 170, 81, 17))
        self.label_3.setObjectName("label_3")
        self.lineEdit = QtWidgets.QLineEdit(Dialog)
        self.lineEdit.setGeometry(QtCore.QRect(20, 190, 271, 27))
        self.lineEdit.setObjectName("lineEdit")
        self.pBSetPath = QtWidgets.QPushButton(Dialog)
        self.pBSetPath.setGeometry(QtCore.QRect(300, 190, 81, 27))
        self.pBSetPath.setObjectName("pBSetPath")
        self.layoutWidget = QtWidgets.QWidget(Dialog)
        self.layoutWidget.setGeometry(QtCore.QRect(20, 20, 361, 29))
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.comboBox = QtWidgets.QComboBox(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBox.sizePolicy().hasHeightForWidth())
        self.comboBox.setSizePolicy(sizePolicy)
        self.comboBox.setObjectName("comboBox")
        self.horizontalLayout.addWidget(self.comboBox)
        self.pBOk = QtWidgets.QPushButton(Dialog)
        self.pBOk.setGeometry(QtCore.QRect(280, 230, 99, 27))
        self.pBOk.setObjectName("pBOk")
        self.pBCancel = QtWidgets.QPushButton(Dialog)
        self.pBCancel.setGeometry(QtCore.QRect(160, 230, 99, 27))
        self.pBCancel.setObjectName("pBCancel")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.RadioHigh.setText(_translate("Dialog", "清晰度最高的"))
        self.RadioLow.setText(_translate("Dialog", "清晰度最低的"))
        self.label_2.setText(_translate("Dialog", "指定清晰度不存在时，默认下载："))
        self.label_3.setText(_translate("Dialog", "保存路径："))
        self.pBSetPath.setText(_translate("Dialog", "设置"))
        self.label.setText(_translate("Dialog", "选择下载的清晰度："))
        self.pBOk.setText(_translate("Dialog", "ok"))
        self.pBCancel.setText(_translate("Dialog", "cancel"))


