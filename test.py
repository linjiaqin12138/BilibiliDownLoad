# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'bilibili.ui'
#
# Created by: PyQt5 UI code generator 5.12
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_BilibiliVideoDownLoad(object):
    def setupUi(self, BilibiliVideoDownLoad):
        BilibiliVideoDownLoad.setObjectName("BilibiliVideoDownLoad")
        BilibiliVideoDownLoad.resize(442, 318)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(BilibiliVideoDownLoad.sizePolicy().hasHeightForWidth())
        BilibiliVideoDownLoad.setSizePolicy(sizePolicy)
        BilibiliVideoDownLoad.setMinimumSize(QtCore.QSize(442, 318))
        BilibiliVideoDownLoad.setMaximumSize(QtCore.QSize(442, 318))
        BilibiliVideoDownLoad.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.centralwidget = QtWidgets.QWidget(BilibiliVideoDownLoad)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setObjectName("centralwidget")
        self.stackedWidget = QtWidgets.QStackedWidget(self.centralwidget)
        self.stackedWidget.setGeometry(QtCore.QRect(0, 0, 442, 331))
        self.stackedWidget.setObjectName("stackedWidget")
        self.MainPage = QtWidgets.QWidget()
        self.MainPage.setObjectName("MainPage")
        self.label = QtWidgets.QLabel(self.MainPage)
        self.label.setGeometry(QtCore.QRect(30, 20, 371, 141))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(3)
        sizePolicy.setVerticalStretch(3)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(29)
        self.label.setFont(font)
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("resources/timg.jpeg"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        self.layoutWidget = QtWidgets.QWidget(self.MainPage)
        self.layoutWidget.setGeometry(QtCore.QRect(40, 190, 361, 91))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.pBDownLoadOne = QtWidgets.QPushButton(self.layoutWidget)
        self.pBDownLoadOne.setStyleSheet("background-color: rgb(44, 163, 205);\n"
"\n"
"")
        self.pBDownLoadOne.setObjectName("pBDownLoadOne")
        self.verticalLayout_2.addWidget(self.pBDownLoadOne)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        self.pBDownLoadMore = QtWidgets.QPushButton(self.layoutWidget)
        self.pBDownLoadMore.setStyleSheet("background-color: rgb(244, 90, 141);")
        self.pBDownLoadMore.setObjectName("pBDownLoadMore")
        self.verticalLayout_2.addWidget(self.pBDownLoadMore)
        self.stackedWidget.addWidget(self.MainPage)
        self.DownLoadOnePage = QtWidgets.QWidget()
        self.DownLoadOnePage.setObjectName("DownLoadOnePage")
        self.lbInputHere = QtWidgets.QLabel(self.DownLoadOnePage)
        self.lbInputHere.setGeometry(QtCore.QRect(20, 20, 141, 17))
        self.lbInputHere.setObjectName("lbInputHere")
        self.lbParserUrl = QtWidgets.QLabel(self.DownLoadOnePage)
        self.lbParserUrl.setGeometry(QtCore.QRect(20, 90, 131, 17))
        self.lbParserUrl.setObjectName("lbParserUrl")
        self.layoutWidget1 = QtWidgets.QWidget(self.DownLoadOnePage)
        self.layoutWidget1.setGeometry(QtCore.QRect(20, 50, 401, 35))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.layoutWidget1)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lEUrlInput = QtWidgets.QLineEdit(self.layoutWidget1)
        self.lEUrlInput.setObjectName("lEUrlInput")
        self.horizontalLayout.addWidget(self.lEUrlInput)
        self.pBUrlConfirm = QtWidgets.QPushButton(self.layoutWidget1)
        self.pBUrlConfirm.setObjectName("pBUrlConfirm")
        self.horizontalLayout.addWidget(self.pBUrlConfirm)
        self.layoutWidget2 = QtWidgets.QWidget(self.DownLoadOnePage)
        self.layoutWidget2.setGeometry(QtCore.QRect(20, 110, 412, 191))
        self.layoutWidget2.setObjectName("layoutWidget2")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget2)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.lbVideoName = QtWidgets.QLabel(self.layoutWidget2)
        self.lbVideoName.setObjectName("lbVideoName")
        self.horizontalLayout_2.addWidget(self.lbVideoName)
        self.lEVideoName = QtWidgets.QLineEdit(self.layoutWidget2)
        self.lEVideoName.setObjectName("lEVideoName")
        self.horizontalLayout_2.addWidget(self.lEVideoName)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.lbPath = QtWidgets.QLabel(self.layoutWidget2)
        self.lbPath.setObjectName("lbPath")
        self.horizontalLayout_3.addWidget(self.lbPath)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
        self.lbCurrentPath = QtWidgets.QLabel(self.layoutWidget2)
        self.lbCurrentPath.setMinimumSize(QtCore.QSize(240, 0))
        self.lbCurrentPath.setObjectName("lbCurrentPath")
        self.horizontalLayout_3.addWidget(self.lbCurrentPath)
        self.pBModiryPath = QtWidgets.QPushButton(self.layoutWidget2)
        self.pBModiryPath.setObjectName("pBModiryPath")
        self.horizontalLayout_3.addWidget(self.pBModiryPath)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.lbQuality = QtWidgets.QLabel(self.layoutWidget2)
        self.lbQuality.setObjectName("lbQuality")
        self.horizontalLayout_4.addWidget(self.lbQuality)
        self.cBQuality = QtWidgets.QComboBox(self.layoutWidget2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cBQuality.sizePolicy().hasHeightForWidth())
        self.cBQuality.setSizePolicy(sizePolicy)
        self.cBQuality.setMinimumSize(QtCore.QSize(2, 0))
        self.cBQuality.setCurrentText("")
        self.cBQuality.setObjectName("cBQuality")
        self.horizontalLayout_4.addWidget(self.cBQuality)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem2)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.pBStartToDownLoad = QtWidgets.QPushButton(self.layoutWidget2)
        self.pBStartToDownLoad.setObjectName("pBStartToDownLoad")
        self.horizontalLayout_5.addWidget(self.pBStartToDownLoad)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem3)
        self.pBReturn = QtWidgets.QPushButton(self.layoutWidget2)
        self.pBReturn.setObjectName("pBReturn")
        self.horizontalLayout_5.addWidget(self.pBReturn)
        self.verticalLayout.addLayout(self.horizontalLayout_5)
        self.stackedWidget.addWidget(self.DownLoadOnePage)
        self.DownLoadMorePage = QtWidgets.QWidget()
        self.DownLoadMorePage.setObjectName("DownLoadMorePage")
        self.lbmessage = QtWidgets.QLabel(self.DownLoadMorePage)
        self.lbmessage.setGeometry(QtCore.QRect(20, 20, 201, 31))
        self.lbmessage.setObjectName("lbmessage")
        self.layoutWidget3 = QtWidgets.QWidget(self.DownLoadMorePage)
        self.layoutWidget3.setGeometry(QtCore.QRect(20, 60, 391, 35))
        self.layoutWidget3.setObjectName("layoutWidget3")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.layoutWidget3)
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.lEUrlMore = QtWidgets.QLineEdit(self.layoutWidget3)
        self.lEUrlMore.setMaximumSize(QtCore.QSize(16777215, 16777214))
        self.lEUrlMore.setObjectName("lEUrlMore")
        self.horizontalLayout_6.addWidget(self.lEUrlMore)
        self.pBparserUrlMore = QtWidgets.QPushButton(self.layoutWidget3)
        self.pBparserUrlMore.setObjectName("pBparserUrlMore")
        self.horizontalLayout_6.addWidget(self.pBparserUrlMore)
        self.videoList = QtWidgets.QScrollArea(self.DownLoadMorePage)
        self.videoList.setGeometry(QtCore.QRect(20, 100, 391, 141))
        self.videoList.setMinimumSize(QtCore.QSize(391, 141))
        self.videoList.setWidgetResizable(True)
        self.videoList.setObjectName("videoList")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 389, 139))
        self.scrollAreaWidgetContents.setMinimumSize(QtCore.QSize(389, 10))
        self.scrollAreaWidgetContents.setAutoFillBackground(False)
        self.scrollAreaWidgetContents.setInputMethodHints(QtCore.Qt.ImhNone)
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.checkBox = QtWidgets.QCheckBox(self.scrollAreaWidgetContents)
        self.checkBox.setGeometry(QtCore.QRect(2, 5, 20, 21))
        self.checkBox.setText("")
        self.checkBox.setObjectName("checkBox")
        self.lineEdit = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.lineEdit.setGeometry(QtCore.QRect(28, 2, 351, 27))
        self.lineEdit.setObjectName("lineEdit")
        self.checkBox_3 = QtWidgets.QCheckBox(self.scrollAreaWidgetContents)
        self.checkBox_3.setGeometry(QtCore.QRect(2, 71, 20, 21))
        self.checkBox_3.setText("")
        self.checkBox_3.setObjectName("checkBox_3")
        self.lineEdit_3 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.lineEdit_3.setGeometry(QtCore.QRect(28, 68, 351, 27))
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.lineEdit_2.setGeometry(QtCore.QRect(28, 35, 351, 27))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.checkBox_2 = QtWidgets.QCheckBox(self.scrollAreaWidgetContents)
        self.checkBox_2.setGeometry(QtCore.QRect(2, 38, 20, 21))
        self.checkBox_2.setText("")
        self.checkBox_2.setObjectName("checkBox_2")
        self.videoList.setWidget(self.scrollAreaWidgetContents)
        self.pBStartToDownLoadMore = QtWidgets.QPushButton(self.DownLoadMorePage)
        self.pBStartToDownLoadMore.setGeometry(QtCore.QRect(20, 250, 99, 27))
        self.pBStartToDownLoadMore.setObjectName("pBStartToDownLoadMore")
        self.pBReturnToMainPageFromMore = QtWidgets.QPushButton(self.DownLoadMorePage)
        self.pBReturnToMainPageFromMore.setGeometry(QtCore.QRect(310, 250, 99, 27))
        self.pBReturnToMainPageFromMore.setObjectName("pBReturnToMainPageFromMore")
        self.stackedWidget.addWidget(self.DownLoadMorePage)
        BilibiliVideoDownLoad.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(BilibiliVideoDownLoad)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 442, 25))
        self.menubar.setObjectName("menubar")
        BilibiliVideoDownLoad.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(BilibiliVideoDownLoad)
        self.statusbar.setObjectName("statusbar")
        BilibiliVideoDownLoad.setStatusBar(self.statusbar)

        self.retranslateUi(BilibiliVideoDownLoad)
        self.stackedWidget.setCurrentIndex(2)
        QtCore.QMetaObject.connectSlotsByName(BilibiliVideoDownLoad)

    def retranslateUi(self, BilibiliVideoDownLoad):
        _translate = QtCore.QCoreApplication.translate
        BilibiliVideoDownLoad.setWindowTitle(_translate("BilibiliVideoDownLoad", "MainWindow"))
        self.pBDownLoadOne.setText(_translate("BilibiliVideoDownLoad", "下载单个视频"))
        self.pBDownLoadMore.setText(_translate("BilibiliVideoDownLoad", "批量下载"))
        self.lbInputHere.setText(_translate("BilibiliVideoDownLoad", "在此输入视频链接："))
        self.lbParserUrl.setText(_translate("BilibiliVideoDownLoad", "解析链接中..."))
        self.pBUrlConfirm.setText(_translate("BilibiliVideoDownLoad", "确定"))
        self.lbVideoName.setText(_translate("BilibiliVideoDownLoad", "视频名称："))
        self.lbPath.setText(_translate("BilibiliVideoDownLoad", "保存路径："))
        self.lbCurrentPath.setText(_translate("BilibiliVideoDownLoad", "./"))
        self.pBModiryPath.setText(_translate("BilibiliVideoDownLoad", "点击修改"))
        self.lbQuality.setText(_translate("BilibiliVideoDownLoad", "清晰度："))
        self.pBStartToDownLoad.setText(_translate("BilibiliVideoDownLoad", "开始下载"))
        self.pBReturn.setText(_translate("BilibiliVideoDownLoad", "返回"))
        self.lbmessage.setText(_translate("BilibiliVideoDownLoad", "批量下载页面中多个视频"))
        self.pBparserUrlMore.setText(_translate("BilibiliVideoDownLoad", "解析"))
        self.pBStartToDownLoadMore.setText(_translate("BilibiliVideoDownLoad", "下载"))
        self.pBReturnToMainPageFromMore.setText(_translate("BilibiliVideoDownLoad", "返回"))


