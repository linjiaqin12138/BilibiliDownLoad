# 主函数文件，程序由这个文件开始运行

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
    def __init__(self):
        
        super(MainWindow,self).__init__()
        self.setupUi(self)
        self.show()
        # 按钮等控件绑定槽函数
        self.pBDownLoadOne.clicked.connect(self.changeToDownLoadOnePage)
        self.pBReturn.clicked.connect(self.changeToMainPage)
        # 隐藏这个标签，暂时没有用到不管它
        self.lbParserUrl.hide()
        self.pBUrlConfirm.clicked.connect(self.parserUrl)
        self.pBModiryPath.clicked.connect(self.ModifyPath)
        self.pBStartToDownLoad.clicked.connect(self.StartToDownLoad)
        # 下载进度窗口对象
        self.Downloading = downloadDialog()
        
    def ModifyPath(self):
        # 路径设置函数
        path = QFileDialog.getExistingDirectory()
        self.lbCurrentPath.setText(path)

    def changeToDownLoadOnePage(self):
        # 切换到下载单个视频的页面
        self.stackedWidget.setCurrentIndex(1)
    
    def changeToMainPage(self):
        # 切换回主页面
        self.stackedWidget.setCurrentIndex(0)
        # 下载视频页面的一些遗留的信息清除掉
        self.cBQuality.clear()
        self.lEUrlInput.clear()
        self.lEVideoName.clear()
        self.lbCurrentPath.clear()

    def parserUrl(self):
        # 解析链接的函数
        # 获取用户输入的链接
        url = self.lEUrlInput.text()
        try:
            # 将链接传递给downloader对象解析
            self.downloader = DownLoader(url)
            # 三个自定义信号的绑定，用来实现下载界面窗口的一些功能（用信号量更新进度条和标签文字等）
            self.downloader.processsignal.trigger.connect(self.Downloading.slotFun)
            self.downloader.processsignal.merge_trigger.connect(self.Downloading.merge)
            self.downloader.processsignal.close_trigger.connect(self.Downloading.CanbeClose)
            #进行下载的解析
            self.downloader.prepare()
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
            # 没有发生异常，将解析到的清晰度、视频名称等显示到对应控件上
            qualitysList = self.downloader.acceptQualitys
            # 清空原来遗留下在的清晰度信息
            self.cBQuality.clear()
            for i in range(len(qualitysList)):
                self.cBQuality.insertItem(i,qualitysList[i])
            # 在输入框显示视频名称
            self.lEVideoName.setText(self.downloader.title)
        
    def StartToDownLoad(self):
        # 开始进行视频的下载
        #获得当前用户选择的清晰度、保存路径、修改后的视频名称等
        stream_id = self.cBQuality.currentText()
        output_dir = self.lbCurrentPath.text()
        title = self.lEVideoName.text()
        # 设置下载窗口的标签控件显示内容
        self.Downloading.lbCur.setText(title)
        self.Downloading.lbDownLoading.setText("下载中")
        # 分配一个线程下载视频，以免阻塞主窗口的运行
        t= threading.Thread(target=self.downloader.startToDownLoad,args=(stream_id,output_dir,title))#创建线程
        t.start()
        # 显示下载界面
        self.Downloading.show()

# 程序入口
if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    a = MainWindow()
    sys.exit(app.exec_())

        
