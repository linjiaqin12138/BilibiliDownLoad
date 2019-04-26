# TODO FUCK blibili
from PyQt5.QtWidgets import QDialog,QMainWindow,QApplication,QFileDialog,QErrorMessage 
from PyQt5.QtGui import QPixmap
from bilibili import Ui_BilibiliVideoDownLoad
from testDownLoadDialog import *
import threading
from DownLoad import *
from moviepy.editor import *
import threading

class MainWindow(QMainWindow,Ui_BilibiliVideoDownLoad):

    def __init__(self):
        super(MainWindow,self).__init__()
        self.setupUi(self)
        self.show()
        self.pBDownLoadOne.clicked.connect(self.changeToDownLoadOnePage)
        self.pBReturn.clicked.connect(self.changeToMainPage)
        self.lbParserUrl.hide()
        self.pBUrlConfirm.clicked.connect(self.parserUrl)
        self.pBModiryPath.clicked.connect(self.ModifyPath)
        self.pBStartToDownLoad.clicked.connect(self.StartToDownLoad)
        self.Downloading = downloadDialog()
        
    def ModifyPath(self):
        path = QFileDialog.getExistingDirectory()
        self.lbCurrentPath.setText(path)

    def changeToDownLoadOnePage(self):
        self.stackedWidget.setCurrentIndex(1)
    
    def changeToMainPage(self):
        self.stackedWidget.setCurrentIndex(0)
        self.cBQuality.clear()
        self.lEUrlInput.clear()
        self.lEVideoName.clear()
        self.lbCurrentPath.clear()

    def parserUrl(self):
        url = self.lEUrlInput.text()
        try:
            self.downloader = DownLoader(url)
            self.downloader.processsignal.trigger.connect(self.Downloading.slotFun)
            self.downloader.processsignal.merge_trigger.connect(self.Downloading.merge)
            self.downloader.processsignal.close_trigger.connect(self.Downloading.CanbeClose)
            #self.Downloading.lbCur.setText(self.downloader.title)
            #self.downloader.processsignal.total_size.connect(self.Downloading.setTotalSize)
            #connect(self.Downloading.slotFun)
            #进行下载的解析
            self.downloader.prepare()
        except MultiplePageError as M:
            error = QErrorMessage(self)
            error.showMessage(M.errorMessage())
            error.show()
        except :
            error = QErrorMessage(self)
            error.showMessage("无法解析链接")
            error.show()
        else:
            qualitysList = self.downloader.acceptQualitys
            self.cBQuality.clear()
            for i in range(len(qualitysList)):
                self.cBQuality.insertItem(i,qualitysList[i])
            self.lEVideoName.setText(self.downloader.title)
        
    def StartToDownLoad(self):
        #获得当前用户选择的清晰度
        stream_id = self.cBQuality.currentText()
        output_dir = self.lbCurrentPath.text()
        title = self.lEVideoName.text()
        self.Downloading.lbCur.setText(title)
        self.Downloading.lbDownLoading.setText("下载中")
        t= threading.Thread(target=self.downloader.startToDownLoad,args=(stream_id,output_dir,title))#创建线程
        t.start()
        self.Downloading.show()

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    a = MainWindow()
    sys.exit(app.exec_())

        
