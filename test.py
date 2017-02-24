import time
from PyQt4 import QtCore
import sys
from PyQt4 import QtGui
import os
import Kmean
import thread
from PIL import Image
from skimage import io

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

img=""
K=10

iterNum=5
class Ui_Form(QtGui.QWidget):
    def __init__(self):
        super(Ui_Form, self).__init__()
        
        self.setupUi()

    def setupUi(self):
	hbox = QtGui.QHBoxLayout(self)
	self.topleft = QtGui.QFrame()
        self.topleft.setFrameShape(QtGui.QFrame.StyledPanel)
   
        self.topright = QtGui.QFrame()
        self.topright.setFrameShape(QtGui.QFrame.StyledPanel)
        self.top = QtGui.QFrame()
        self.top.setFrameShape(QtGui.QFrame.StyledPanel)

	
        self.splitter1 = QtGui.QSplitter(QtCore.Qt.Horizontal)
        self.splitter1.addWidget(self.topleft)
        self.splitter1.addWidget(self.topright)
        self.splitter1.setSizes([20,80])

        self.splitter2 = QtGui.QSplitter(QtCore.Qt.Vertical)
	self.splitter2.addWidget(self.top)
        self.splitter2.addWidget(self.splitter1)
        self.splitter2.setSizes([30,80])

	self.answer1 = QtGui.QLabel()
        q1Edit = QtGui.QLineEdit(self.top)
        q1Edit.textChanged.connect(self.q1Changed)
	q1Edit.setGeometry(920,10,40,25)
	self.NumIte = QtGui.QLabel(self.top)
	self.NumIte.setGeometry(800,7,100,40)
	self.NumIte.setText("Iteration Value:")

        self.answer2 = QtGui.QLabel()
        q2Edit = QtGui.QLineEdit(self.top)
        q2Edit.textChanged.connect(self.q2Changed)
	q2Edit.setGeometry(920,50,40,25)
	self.Kvalue = QtGui.QLabel(self.top)
	self.Kvalue.setGeometry(820,40,100,40)
	self.Kvalue.setText("K Value :")

        self.progressBar = QtGui.QProgressBar(self.topright)
        self.progressBar.setGeometry(QtCore.QRect(100, 13, 508, 23))
        self.progressBar.setProperty("value", 10)
        self.progressBar.setTextVisible(False)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))

	self.pic = QtGui.QLabel(self.topright)
	self.pic.setGeometry(10, 20, 350, 400)
	self.pic2 = QtGui.QLabel(self.topright)
	self.pic2.setGeometry(380, 20, 350, 400)	
	
        self.runButton = QtGui.QPushButton("run",self.topright)
        self.runButton.setGeometry(QtCore.QRect(20, 10, 70, 30))
        self.runButton.setObjectName(_fromUtf8("runButton"))
        self.runButton.clicked.connect(self.onStart)
	
	open_btn = QtGui.QPushButton('Open', self.top)
        open_btn.resize(170,40)
        open_btn.move(25, 10)  
	open_btn.clicked.connect(self.showDialog)
	self.fileText = QtGui.QLabel(self.top)
	self.fileText.setGeometry(205,10,500,40)

	self.inputfile = QtGui.QLabel(self.topright)
	self.inputfile.setGeometry(20,425,200,40)
	self.runingAlgo = QtGui.QLabel(self.topright)
	self.runingAlgo.setGeometry(620,7,200,40)
	self.runingAlgo.setText("Choose file")
	self.inputfile.setText("INPUT IMAGE ")
	self.outputfile = QtGui.QLabel(self.topright)
	self.outputfile.setGeometry(390,425,200,40)
	self.outputfile.setText("OUTPUT IMAGE")

	

        openFile = QtGui.QAction(QtGui.QIcon('open.png'), 'Open', self.top)
        openFile.setShortcut('Ctrl+O')
        openFile.setStatusTip('Open new File')
        openFile.triggered.connect(self.showDialog)

        """menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(openFile)"""

        self.myLongTask = TaskThread()
        self.myLongTask.taskFinished.connect(self.onFinished)

	hbox.addWidget(self.splitter2)
		
      	self.setLayout(hbox)
      	QtGui.QApplication.setStyle(QtGui.QStyleFactory.create('Cleanlooks'))
		

        self.setGeometry(100, 100, 1000, 800)
        self.setWindowTitle('Image Segmentation tool kit')
        self.show()

    def onStart(self): 
	global img,K,iterNum
	try:
            K=int(self.returnAnswer1())
	    iterNum=int(self.returnAnswer2())
	except:
	    self.runingAlgo.setText("Error: Wrong Option :")
	    return
	print K,iterNum
	if img!="" :
            self.progressBar.setRange(0,0)
	    self.runingAlgo.setText(" Running....")
            self.myLongTask.start()
	else:
	    self.runingAlgo.setText("No file choosen...")


    def onFinished(self):
        # Stop the pulsation
	self.runingAlgo.setText(" Done !")
        self.progressBar.setRange(0,1)
	pixmap = QtGui.QPixmap(os.getcwd()+"/test.jpg")
	pixmap3 = pixmap.scaled(300,300, QtCore.Qt.KeepAspectRatio)
	self.pic2.setPixmap(pixmap3)

	

    def showDialog(self):
        self.fname = QtGui.QFileDialog.getOpenFileName(self, 'Open file', os.getcwd())
	global img
	img=self.fname
        self.fileText.setText(str(img))
	pixmap = QtGui.QPixmap(self.fname)
	pixmap3 = pixmap.scaled(300,300, QtCore.Qt.KeepAspectRatio)
	self.pic.setPixmap(pixmap3)

    def q1Changed(self, text):
        self.answer1.setText(text)

    def q2Changed(self, text):
        self.answer2.setText(text)

    def test(self):
        for i in xrange(500000):
            print i

    def returnAnswer1(self):
        return self.answer1.text()

    def returnAnswer2(self):
        return self.answer2.text()

class TaskThread(QtCore.QThread):
    taskFinished = QtCore.pyqtSignal()
    def run(self):
	global img,K,iterNum
	li=img.split('/')     
        file1=li[len(li)-1] 
        data=io.imread(str(img))
	data=Kmean.kmean(data,K,iterNum)
	im = Image.fromarray(data)
	im.save(os.getcwd()+"/test.jpg")
        self.taskFinished.emit()  

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    ui = Ui_Form()
 
    ui.show()
    sys.exit(app.exec_())
