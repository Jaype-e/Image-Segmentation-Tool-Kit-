import time
from PyQt4 import QtCore
import sys
from PyQt4 import QtGui
import os
import Kmean
import Region_grow
import graph_based
import thread
import GlobalThresholding
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
delta=0
iterNum=5
Num_par=2
sigma=0
mean_size=1
K_graph=1000
row=1
col=23
thre=12
algo_index=1

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
	

	self.header_top_left = QtGui.QLabel(self.topleft)
	self.header_top_left.setGeometry(3,3,180,40)
	self.header_top_left.setText("<font color='#0000c6' > <h3>VARIABLES :-</h3></font>")

	self.answer1 = QtGui.QLabel()
        q1Edit = QtGui.QLineEdit(self.topleft)
        q1Edit.textChanged.connect(self.q1Changed)
	q1Edit.setGeometry(115,40,50,20)
	self.var1 = QtGui.QLabel(self.topleft)
	self.var1.setGeometry(5,30,100,40)
	self.var1.setText("<font color='#97bf0d' > <h4>Iteration Value :</h4></font>")

        self.answer2 = QtGui.QLabel()
        q2Edit = QtGui.QLineEdit(self.topleft)
        q2Edit.textChanged.connect(self.q2Changed)
	q2Edit.setGeometry(115,80,50,20)
	self.var2 = QtGui.QLabel(self.topleft)
	self.var2.setGeometry(5,70,100,40)
	self.var2.setText("<font color='#97bf0d' > <h4>K Value :</h4></font>")

	self.answer3 = QtGui.QLabel()
        q3Edit = QtGui.QLineEdit(self.topleft)
        q3Edit.textChanged.connect(self.q3Changed)
	q3Edit.setGeometry(115,120,50,20)
	self.var3 = QtGui.QLabel(self.topleft)
	self.var3.setGeometry(5,110,100,40)
	self.var3.setText("<font color='#97bf0d' > <h4>Variable3 :</h4></font>")

	self.b1 = QtGui.QRadioButton(self.top)
	self.b1.setStyleSheet('QRadioButton {background-color: #feb4b1; color: blue;}')
	self.b1.setText("K-mean Algorithm")
        self.b1.setChecked(True)
        self.b1.toggled.connect(lambda:self.btnstate(self.b1))
	self.b1.setGeometry(10,50,200,40)

	
	self.b2 = QtGui.QRadioButton(self.top)
	self.b2.setStyleSheet('QRadioButton {background-color: #feb4b1; color: blue;}')
	self.b2.setText("Global Thresholding")
        self.b2.toggled.connect(lambda:self.btnstate(self.b2))
	self.b2.setGeometry(10,90,200,40)

	self.b3 = QtGui.QRadioButton(self.top)
	self.b3.setStyleSheet('QRadioButton {background-color: #feb4b1; color: blue;}')
	self.b3.setText("Regin Grow Method")
        self.b3.toggled.connect(lambda:self.btnstate(self.b3))
	self.b3.setGeometry(10,130,200,40)

	self.b4 = QtGui.QRadioButton(self.top)
	self.b4.setStyleSheet('QRadioButton {background-color: #feb4b1; color: blue;}')
	self.b4.setText("Graph Based Method")
        self.b4.toggled.connect(lambda:self.btnstate(self.b4))
	self.b4.setGeometry(250,50,200,40)

	self.b5 = QtGui.QRadioButton(self.top)
	self.b5.setStyleSheet('QRadioButton {background-color: #feb4b1; color: blue;}')
	self.b5.setText("Otsu Method")
        self.b5.toggled.connect(lambda:self.btnstate(self.b5))
	self.b5.setGeometry(250,90,200,40)

	self.b6 = QtGui.QRadioButton(self.top)
	self.b6.setStyleSheet('QRadioButton {background-color: #feb4b1; color: blue;}')
	self.b6.setText("Watershed Method")
        self.b6.toggled.connect(lambda:self.btnstate(self.b6))
	self.b6.setGeometry(250,130,200,40)

	self.DisText = QtGui.QLabel(self.top)
	self.DisText.setGeometry(500,10,480,200)
	self.DisText.setText("<font color='blue' > <h1> K-mean Algorithm </h1></font><font color='#97bf0d' > <h3>There are some information about this algorithm like<br/> K value needed or something else</h3></font>")
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
	self.runButton.setStyleSheet('QPushButton {background-color: #A3C1DA; color: red;}')
        self.runButton.setGeometry(QtCore.QRect(20, 10, 70, 30))
        self.runButton.setObjectName(_fromUtf8("runButton"))
        self.runButton.clicked.connect(self.onStart)
	
	open_btn = QtGui.QPushButton('Open', self.top)
	open_btn.setStyleSheet('QPushButton {background-color: #A3C1DA; color: red;}')
        open_btn.resize(80,30)
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
	global img,algo_index
	try:
	    if algo_index==1:
	        global K,iterNum
                K=int(self.returnAnswer1())
	        iterNum=int(self.returnAnswer2())
	    elif algo_index==2:
	        global Num_par,delta
                Num_par=int(self.returnAnswer1())
	        delta=int(self.returnAnswer2())
	    elif algo_index==3:
	        global row,col,thre
                row=int(self.returnAnswer1())
	        col=int(self.returnAnswer2())
		thre=int(self.returnAnswer3())
	    elif algo_index==4:
	        global sigma,K_graph,mean_size
                sigma=int(self.returnAnswer1())
	        K_graph=int(self.returnAnswer2())
		mean_size=int(self.returnAnswer3())
	    elif algo_index==5:
	        global K,iterNum
                K=int(self.returnAnswer1())
	        iterNum=int(self.returnAnswer2())
	    elif algo_index==6:
	        global K,iterNum
                K=int(self.returnAnswer1())
	        iterNum=int(self.returnAnswer2())
	except:
	    self.runingAlgo.setText("Error: Wrong Option :")
	    return
	
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

    def q3Changed(self, text):
        self.answer3.setText(text)

    def returnAnswer1(self):
        return self.answer1.text()

    def returnAnswer2(self):
        return self.answer2.text()

    def returnAnswer3(self):
        return self.answer3.text()

    def btnstate(self,b):
	
      	if b.text() == "K-mean Algorithm":
	    if b.isChecked() == True:
		global algo_index
		algo_index=1
		self.var1.setText("<font color='#97bf0d' > <h4>Iteration Value :</h4></font>")
		self.var2.setText("<font color='#97bf0d' > <h4>K Value :</h4></font>")
		self.var3.setText("<font color='#97bf0d' > <h4>variable3 :</h4></font>")
                self.DisText.setText("<font color='blue' > <h1> K-mean Algorithm </h1></font><font color='#97bf0d' > <h3>There are some information about this algorithm like<br/> K value needed or something else</h3></font>")
	elif b.text() == "Global Thresholding":
	    if b.isChecked() == True:
		global algo_index
		algo_index=2
		self.var1.setText("<font color='#97bf0d' > <h4>N value :</h4></font>")
		self.var2.setText("<font color='#97bf0d' > <h4>Delta Value :</h4></font>")
		self.var3.setText("<font color='#97bf0d' > <h4>variable3 :</h4></font>")
                self.DisText.setText("<font color='blue' > <h1> Global Thresholding </h1></font><font color='#97bf0d' > <h3>There are some information about this algorithm like<br/> K value needed or something else</h3></font>")
	elif b.text() == "Regin Grow Method":
	    if b.isChecked() == True:
		global algo_index
		algo_index=3
		self.var1.setText("<font color='#97bf0d' > <h4>Row Value :</h4></font>")
		self.var2.setText("<font color='#97bf0d' > <h4>Col Value :</h4></font>")
		self.var3.setText("<font color='#97bf0d' > <h4>Threshold :</h4></font>")
                self.DisText.setText("<font color='blue' > <h1> Regin Grow Method </h1></font><font color='#97bf0d' > <h3>There are some information about this algorithm like<br/> K value needed or something else</h3></font>")
	elif b.text() == "Graph Based Method":
	    if b.isChecked() == True:
		global algo_index
		algo_index=4
		self.var1.setText("<font color='#97bf0d' > <h4>Sigma Value :</h4></font>")
		self.var2.setText("<font color='#97bf0d' > <h4>K Value :</h4></font>")
		self.var3.setText("<font color='#97bf0d' > <h4>Mean Size :</h4></font>")
                self.DisText.setText("<font color='blue' > <h1> Graph Based Method </h1></font><font color='#97bf0d' > <h3>There are some information about this algorithm like<br/> K value needed or something else</h3></font>")
	elif b.text() == "Otsu Method":
	    if b.isChecked() == True:
		global algo_index
		algo_index=5
		self.var1.setText("<font color='#97bf0d' > <h4>Variable1 :</h4></font>")
		self.var2.setText("<font color='#97bf0d' > <h4>Variable2 :</h4></font>")
		self.var3.setText("<font color='#97bf0d' > <h4>Variable3 :</h4></font>")
                self.DisText.setText("<font color='blue' > <h1> Otsu Method </h1></font><font color='#97bf0d' > <h3>There are some information about this algorithm like<br/> K value needed or something else</h3></font>")
	elif b.text() == "Watershed Method":
	    if b.isChecked() == True:
		global algo_index
		algo_index=6
		self.var1.setText("<font color='#97bf0d' > <h4>Variable1 :</h4></font>")
		self.var2.setText("<font color='#97bf0d' > <h4>Variable2 :</h4></font>")
		self.var3.setText("<font color='#97bf0d' > <h4>Variable3 :</h4></font>")
                self.DisText.setText("<font color='blue' > <h1> Watershed Method </h1></font><font color='#97bf0d' > <h3>There are some information about this algorithm like<br/> K value needed or something else</h3></font>")
      
      
	

class TaskThread(QtCore.QThread):
    taskFinished = QtCore.pyqtSignal()
    def run(self):
	global img,algo_index
	li=img.split('/')     
        file1=li[len(li)-1] 
	if algo_index==1:
	    global K,iterNum
	    data=io.imread(str(img))
	    data=Kmean.kmean(data,iterNum,K)
	elif algo_index==2:
	    global Num_par,delta
	    data=io.imread(str(img))
	    data=GlobalThresholding.global_threshold(data,Num_par,delta)
	elif algo_index==3:
	    global row,col,thre
	    data=io.imread(str(img))
	    data=Region_grow.region_grow_priorityQ(data,[row,col],thre)
	elif algo_index==4:
	    global sigma,mean_size,K_graph
	    print K_graph
	    data=io.imread(str(img))
	    data=graph_based.graph_based_seg(data,mean_size,K_graph,sigma)
	elif algo_index==5:
	    global K,iterNum
	    data=io.imread(str(img))
	    data=Kmean.kmean(data,iterNum,K)
	elif algo_index==6:
	    global K,iterNum
	    data=io.imread(str(img))
	    data=Kmean.kmean(data,iterNum,K)
	im = Image.fromarray(data)
	im.save(os.getcwd()+"/test.jpg")
        self.taskFinished.emit()  

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    ui = Ui_Form()
 
    ui.show()
    sys.exit(app.exec_())
