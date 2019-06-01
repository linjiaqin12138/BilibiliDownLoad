from downloadDialog import *
import setpage
from PyQt5.QtWidgets import QDialog,QMainWindow,QApplication,QFileDialog,QErrorMessage
from PyQt5.QtGui import QIcon
import os
class downloadDialog(QDialog,Ui_Dialog):
    def __init__(self):
        super(downloadDialog,self).__init__()
        self.setupUi(self)
        self.setWindowTitle("等待下载完成")
        self.setWindowIcon(QIcon("./resources/icon.png"))
        #进度条数值设为0
        self.Progress.setValue(0)
    def slotFun(self,value):
        # 更新进度条数值
        self.Progress.setValue(value)
    def settitle(self,title):
        self.lbDownLoading.setText("下载中")
        self.lbCur.setText("当前下载 "+title)
    def merge(self):
        self.lbDownLoading.setText("下载完成")
        self.lbCur.setText("正在进行格式转换，这需要一定的时间")
    
    def CanbeClose(self):
        self.lbCur.setText("格式转换成功，关闭窗口然后去看看吧")

    def setTotalSize(self,value):
        # 设置大小标签
        self.TotalSize = value/1024/1024
        self.Progress.setRange(0,self.TotalSize)

class setpageDialog(QDialog,setpage.Ui_Dialog):
    path = None
    def __init__(self,mainWindow):
        super(setpageDialog,self).__init__()
        self.setupUi(self)
        self.RadioLow.setChecked(True)
        self.setWindowTitle("设置")
        self.setWindowIcon(QIcon("./resources/icon.png"))
        self.comboBox.clear()
        cwd = os.getcwd()
        cwd = cwd.replace('\\','/')
        self.path = cwd
        self.lineEdit.setText(cwd)
        self.pBSetPath.clicked.connect(self.setPath)
        self.pBOk.clicked.connect(mainWindow.StartToDownLoadMore)
        self.pBCancel.clicked.connect(self.close)
    def setPath(self):
        self.path = QFileDialog.getExistingDirectory()
        self.lineEdit.setText(self.path)
    

    def get_path(self):
        return self.path
        


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    a = downloadDialog()
    sys.exit(app.exec_())

