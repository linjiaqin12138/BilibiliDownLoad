from downloadDialog import *
from PyQt5.QtWidgets import QDialog,QMainWindow,QApplication,QFileDialog,QErrorMessage

class downloadDialog(QDialog,Ui_Dialog):
    def __init__(self):
        super(downloadDialog,self).__init__()
        self.setupUi(self)
        #进度条数值设为0
        self.Progress.setValue(0)
        
        
    def slotFun(self,value):
        # 更新进度条数值
        self.Progress.setValue(value)

    def merge(self):
        self.lbDownLoading.setText("下载完成")
        self.lbCur.setText("正在进行格式转换，这需要一定的时间")
    
    def CanbeClose(self):
        self.lbCur.setText("格式转换成功，关闭窗口然后去看看吧")

    def setTotalSize(self,value):
        # 设置大小标签
        self.TotalSize = value/1024/1024
        self.Progress.setRange(0,self.TotalSize)


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    a = downloadDialog()
    sys.exit(app.exec_())

