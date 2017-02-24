import sys
from PyQt4 import QtGui
import os
import Kmean
import thread
from PIL import Image
from skimage import io


class AlgoResult(QtGui.QMainWindow):
    
    def __init__(self,fname):
        super(AlgoResult, self).__init__()
        self.fname=fname
        self.initUI()
        
    def initUI(self):      
	self.pic = QtGui.QLabel(self)
	self.pic.setGeometry(10, 60, 400, 800)
	self.pic2 = QtGui.QLabel(self)
	self.pic2.setGeometry(510, 60, 400, 800)

	li=self.fname.split('/')     
	self.pic.setPixmap(QtGui.QPixmap(self.fname) )
        file1=li[len(li)-1] 
        data=io.imread(str(self.fname))
	data=Kmean.kmean(data,10,5)
	im = Image.fromarray(data)
	im.save(os.getcwd()+"/test.jpg")
	self.pic2.setPixmap(QtGui.QPixmap(os.getcwd()+"/test.jpg") )      
        
        self.setGeometry(120, 100, 900, 900)
        self.setWindowTitle('File dialog')
        self.show()



def result(fname):
    app = QtGui.QApplication(sys.argv)
    ex = AlgoResult(fname)
    sys.exit(app.exec_())



