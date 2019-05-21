from downloadDialog import *
from PyQt5.QtWidgets import QDialog,QMainWindow,QApplication,QFileDialog,QErrorMessage

class downloadDialog(QDialog,Ui_Dialog):
    def __init__(self):
        super(downloadDialog,self).__init__()
        self.setupUi(self)
        self.Progress.setValue(0)
       # self.TotalSize = 0
        
        
    def slotFun(self,value):
        self.Progress.setValue(value)
        #self.Progress.setRange(value/100*self.TotalSize,self.TotalSize)

    def merge(self):
        self.lbDownLoading.setText("下载完成")
        self.lbCur.setText("正在进行格式转换，这需要一定的时间")
    
    def CanbeClose(self):
        self.lbCur.setText("格式转换成功，关闭窗口然后去看看吧")

    def setTotalSize(self,value):
        self.TotalSize = value/1024/1024
        self.Progress.setRange(0,self.TotalSize)


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    a = downloadDialog()
    sys.exit(app.exec_())

