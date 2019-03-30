from PyQt5.QtWidgets import QDialog,QMainWindow,QApplication,QFileDialog,QErrorMessage
from PyQt5.QtGui import QPixmap
from bilibili import Ui_MainWindow
from you_get import common
import threading
import time
class MainWindow(QMainWindow,Ui_MainWindow):

    def __init__(self):
        super(MainWindow,self).__init__()
        self.setupUi(self)
        self.show()
        #pself.lable.setPixmap()
        self.pushButton.clicked.connect(self.printLineEdit)
        self.lineEditChangeFlag = False
        self.lineEdit.setStyleSheet("QLineEdit{color:rgb(161, 161, 161)}\n")
        self.lineEdit.setText("在这里输入链接")
        self.lineEdit.selectionChanged.connect(self.LineInputMode)
        self.lineEdit.editingFinished.connect(self.lineEditReset)
        self.FilePathError = False
        self.UrlError = False
        self.Finish = False
        self.Downloading = False
    #for test    
    def printMessage(self):
        print("test")
        #如果输入框的内容为空,就提示在这里输入链接
    def printLineEdit(self):
        url = self.lineEdit.text()
        #print(type(url))
        url = url.strip()
        file_path = QFileDialog.getExistingDirectory()
        #self.download(url,file_path)
        t = threading.Thread(target=self.download,args=(url,file_path))
        t.start()
        time.sleep(2)
        while(self.Downloading):
            if self.FilePathError:
                self.FilePathError = False
                #raise FileNotFoundError
                error = QErrorMessage(self)
                error.showMessage("文件路径异常")
                break
            elif self.UrlError:
                self.UrlError = False
                #raise TypeError
                error = QErrorMessage(self)
                error.showMessage("输入链接错误")
                break
            
        #common.any_download(url=url,ext="mp4",merge=True,output_dir=file_path)

    def download(self,url,output_dir,ext=None,merge=True):
        try:
            self.Downloading = True
            common.any_download(url=url,ext=ext,merge=merge,output_dir=output_dir)
            time.sleep(2)
            self.Downloading = False
            self.Finish = True
        except FileNotFoundError:
            self.FilePathError = True
        except TypeError:
            self.UrlError = True
        
    def LineInputMode(self):
        if not self.lineEditChangeFlag:
            self.lineEdit.setStyleSheet("QLineEdit{color:rgb(0, 0, 0)}\n")
            self.lineEdit.setText(" ")
            self.lineEditChangeFlag = True
    def lineEditReset(self):
        if(len(self.lineEdit.text())==0):
            self.lineEdit.setStyleSheet("QLineEdit{color:rgb(161, 161, 161)}\n")
            self.lineEdit.setText("在这里输入链接")
            self.lineEditChangeFlag = False
        else:
            #print(self.lineEdit.text())
            pass
    

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    a = MainWindow()
    sys.exit(app.exec_())

        
