# 主函数文件，程序由这个文件开始运行
from PyQt5 import QtWidgets,QtGui

# 用到的Qt相关的库
from PyQt5.QtWidgets import QDialog,QMainWindow,QApplication,QFileDialog,QErrorMessage 

from PyQt5.QtGui import QPixmap
# 导入由QT的pyuic5命令生成的主界面类
from bilibili import Ui_BilibiliVideoDownLoad

# 下载过程中的进度条窗口界面类
from testDownLoadDialog import *
# 多线程库
import threading
# 自写的下载视频的爬虫库
from DownLoad import *
# 格式转换库
from moviepy.editor import *

class MainWindow(QMainWindow,Ui_BilibiliVideoDownLoad):
    videoselectlist = []
    def __init__(self):  
        super(MainWindow,self).__init__()
        self.setupUi(self)
        self.show()
        # 下载进度窗口对象
        self.Downloading = downloadDialog()
        # 批量下载设置窗口
        self.setPage = setpageDialog()
        # 按钮等控件绑定槽函数
        # 下载单个视频的按钮
        self.pBDownLoadOne.clicked.connect(self.changeToDownLoadOnePage)
        # 批量下载视频的按钮
        self.pBDownLoadMore.clicked.connect(self.changeToDownLoadMorePage)
        # 下载单个视频的页面返回主页面的按钮
        self.pBReturn.clicked.connect(self.changeToMainPage)
        # 从批量下载页面返回主页面的按钮
        self.pBReturnToMainPageFromMore.clicked.connect(self.changeToMainPage)
        # 下载单个视频页面解析链接的按钮
        self.pBUrlConfirm.clicked.connect(self.parserUrl)
        # 批量下载视频页面解析链接的按钮
        self.pBparserUrlMore.clicked.connect(self.parserUrl)
        # 下载单个视频页面保存路径按钮
        self.pBModiryPath.clicked.connect(self.ModifyPath)
        # 下载单个视频页面的下载按钮
        self.pBStartToDownLoad.clicked.connect(self.StartToDownLoadOne)
        # 批量下载页面下载按钮
        self.pBStartToDownLoadMore.clicked.connect(self.setPage.show)
        
        # 隐藏这个标签，暂时没有用到不管它
        self.lbParserUrl.hide()
        
        # 下载列表初始
        # 解析出来的视频列表的选择框和编辑窗口的水平布局控件列表
        self.videoselectlist.clear()
        # 重新滚动窗口内容的控件
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(10,10,370,10))
        self.videoList.setWidgetResizable(True)
     
    def ModifyPath(self):
        # 路径设置函数
        path = QFileDialog.getExistingDirectory()
        self.lbCurrentPath.setText(path)

    def changeToDownLoadOnePage(self):
        # 切换到下载单个视频的页面
        self.stackedWidget.setCurrentIndex(1)
    
    def changeToDownLoadMorePage(self):
        self.stackedWidget.setCurrentIndex(2)

    def changeToMainPage(self):
        # 切换回主页面
        #print(self.stackedWidget.currentIndex)
        if self.stackedWidget.currentIndex() == 1:
            # 下载视频页面的一些遗留的信息清除掉
            self.cBQuality.clear()
            self.lEUrlInput.clear()
            self.lEVideoName.clear()
            self.lbCurrentPath.clear()
        elif self.stackedWidget.currentIndex() == 2:
            # 清空水平布局控件列表，但他们还没有失去引用
            self.videoselectlist.clear()
            # 更新滚动区控件，相当于清空，原来的对象失去引用释放内存
            self.scrollAreaWidgetContents = QtWidgets.QWidget()
            self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(10,10,370,10))
            self.videoList.setWidgetResizable(True)
            self.videoList.setWidget(self.scrollAreaWidgetContents)
            self.lEUrlMore.clear()
        self.stackedWidget.setCurrentIndex(0)
        
        

    def parserUrl(self):
        # 解析链接的函数
        # 获取用户输入的链接
        url = self.lEUrlInput.text()
        if len(url)==0:
            url = self.lEUrlMore.text()
        if len(url)==0:
            error = QErrorMessage(self)
            error.showMessage("无法解析链接")
            error.show()
            return 
        try:
            # 将链接传递给downloader对象解析
            self.downloader = DownLoader(url)
            # 三个自定义信号的绑定，用来实现下载界面窗口的一些功能（用信号量更新进度条和标签文字等）
            self.downloader.processsignal.trigger.connect(self.Downloading.slotFun)
            self.downloader.processsignal.merge_trigger.connect(self.Downloading.merge)
            self.downloader.processsignal.close_trigger.connect(self.Downloading.CanbeClose)
            #进行下载的解析
            self.downloader.prepare(self.stackedWidget.currentIndex())
        # 处理异常情况并弹出窗口提示
        except MultiplePageError as M:
            # 链接包含多个视频，要转到批量下载界面（还没做）
            error = QErrorMessage(self)
            error.showMessage(M.errorMessage())
            error.show()
        except :
            # 未知错误
            error = QErrorMessage(self)
            error.showMessage("无法解析链接")
            error.show()
        else:
            if self.stackedWidget.currentIndex() == 1:
                # 没有发生异常，将解析到的清晰度、视频名称等显示到对应控件上
                qualitysList = self.downloader.acceptQualitys
                # 清空原来遗留下在的清晰度信息
                self.cBQuality.clear()
                for i in range(len(qualitysList)):
                    self.cBQuality.insertItem(i,qualitysList[i])
                # 在输入框显示视频名称
                self.lEVideoName.setText(self.downloader.title)
            else:
                #pn = downloader.get_pageN()
                titles = self.downloader.get_titles()
                pn = len(titles)
                self.scrollAreaWidgetContents = QtWidgets.QWidget()
                self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(10,10,370,10+33*pn))
                self.scrollAreaWidgetContents.setMinimumHeight(10+33*pn)
                self.videoList.setWidgetResizable(True)
                for i in range(pn):
                    checkBox = QtWidgets.QCheckBox(self.scrollAreaWidgetContents)
                    checkBox.setGeometry(2,5+33*i,20,21)
                    checkBox.setText("")
                    checkBox.setObjectName("checkBox"+str(i))
                    #horizontalLayout.addWidget(checkBox)
                    lineEdit = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
                    lineEdit.setGeometry(28,2+33*i,351,27)
                    lineEdit.setObjectName("lineEdit"+str(i))
                    lineEdit.setText(titles[i])
                    self.videoselectlist.append([checkBox,lineEdit])
                self.videoList.setWidget(self.scrollAreaWidgetContents)
                #checkBox.isChecked()
                
    # 开始下载单条视频   
    def StartToDownLoadOne(self):
        # 开始进行视频的下载
        #获得当前用户选择的清晰度、保存路径、修改后的视频名称等
        stream_id = self.cBQuality.currentText()
        output_dir = self.lbCurrentPath.text()
        title = self.lEVideoName.text()
        # 设置下载窗口的标签控件显示内容
        self.Downloading.lbCur.setText(title)
        self.Downloading.lbDownLoading.setText("下载中")
        # 分配一个线程下载视频，以免阻塞主窗口的运行
        t= threading.Thread(target=self.downloader.startToDownLoadOne,args=(stream_id,output_dir,title))#创建线程
        t.start()
        # 显示下载界面
        self.Downloading.show()
    def StartToDownLoadMore(self):
        # 读取设置页面选项
        output_dir = self.setPage.get_path()
        stream_id = self.setPage.comboBox.currentText()
        optionHigh = self.setPage.RadioHigh.isChecked() 
        # 获得被选中的下载的视频列表
        videoIndexAndtitleList = []
        for i,[cBox,lEdit] in enumerate(self.videoselectlist):
            if cBox.isChecked():
                videoIndexAndtitleList.append([i,lEdit.currentText()])
                print(lEdit.currentText())
        t = threading.Thread(target=self.downloader.StartToDOwnLoadMore,args=(stream_id,output_dir,videoIndexAndtitleList))
        t.start()
        self.Downloading.show()
# 程序入口
if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    splash = QtWidgets.QSplashScreen(QtGui.QPixmap('./resources/logo.png'))
    splash.show()
    splash.showMessage("正在加载")
    import time
    time.sleep(2)
    a = MainWindow()
    splash.close()
    sys.exit(app.exec_())

        
