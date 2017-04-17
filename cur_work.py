import time
from PyQt4 import QtCore
import sys
from PyQt4 import QtGui
import os
import Kmean
import Region_grow
import graph_based
import thread
import otsu
import Err
import fuzzy
import GlobalThresholding
from PIL import Image
from skimage import io
import matplotlib.pyplot as plt
import numpy as np

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
grd_img=""
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
file1=""
file2=""

def rgb2gray(rgb):
    return np.dot(rgb[...,:3], [0.299, 0.587, 0.114])

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
        self.splitter1.setSizes([41,59])

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
	self.var1.setGeometry(5,30,105,40)
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

	self.Img_inf = QtGui.QLabel(self.topleft)
	self.Img_inf.setGeometry(5,150,180,200)

	self.b1 = QtGui.QRadioButton(self.top)
	self.b1.setStyleSheet('QRadioButton {background-color: #feb0b1; color: blue;}')
	self.b1.setText("K-mean Algorithm")
        self.b1.setChecked(True)
        self.b1.toggled.connect(lambda:self.btnstate(self.b1))
	self.b1.setGeometry(10,50,200,30)

	
	self.b2 = QtGui.QRadioButton(self.top)
	self.b2.setStyleSheet('QRadioButton {background-color: #fec0b1; color: blue;}')
	self.b2.setText("Global Thresholding")
        self.b2.toggled.connect(lambda:self.btnstate(self.b2))
	self.b2.setGeometry(10,80,200,30)

	self.b3 = QtGui.QRadioButton(self.top)
	self.b3.setStyleSheet('QRadioButton {background-color: #feb0b1; color: blue;}')
	self.b3.setText("Regin Grow Method")
        self.b3.toggled.connect(lambda:self.btnstate(self.b3))
	self.b3.setGeometry(10,110,200,30)

	self.b4 = QtGui.QRadioButton(self.top)
	self.b4.setStyleSheet('QRadioButton {background-color: #fec0b1; color: blue;}')
	self.b4.setText("Graph Based Method")
        self.b4.toggled.connect(lambda:self.btnstate(self.b4))
	self.b4.setGeometry(250,50,200,30)

	self.b5 = QtGui.QRadioButton(self.top)
	self.b5.setStyleSheet('QRadioButton {background-color: #feb0b1; color: blue;}')
	self.b5.setText("Otsu Method")
        self.b5.toggled.connect(lambda:self.btnstate(self.b5))
	self.b5.setGeometry(250,80,200,30)

	self.b6 = QtGui.QRadioButton(self.top)
	self.b6.setStyleSheet('QRadioButton {background-color: #fec0b1; color: blue;}')
	self.b6.setText("Watershed Method")
        self.b6.toggled.connect(lambda:self.btnstate(self.b6))
	self.b6.setGeometry(250,110,200,30)

	self.b7 = QtGui.QRadioButton(self.top)
	self.b7.setStyleSheet('QRadioButton {background-color: #fec0b1; color: blue;}')
	self.b7.setText("Fuzzy C-Mean")
        self.b7.toggled.connect(lambda:self.btnstate(self.b7))
	self.b7.setGeometry(10,140,200,30)

	self.DisText = QtGui.QLabel(self.top)
	self.DisText.setGeometry(500,10,480,200)
	self.DisText.setText("<font color='blue' > <h1> K-mean Algorithm </h1></font><font color='#97bf0d' > <h3>This algorithm uses to find K cluster in image. For which <br/> you have to select K value and Iteration value .If you <br> have no idea than select K = 5 and iterarion no more then<br> 10.<br></h3></font>")
        self.progressBar = QtGui.QProgressBar(self.topright)
        self.progressBar.setGeometry(QtCore.QRect(100, 13, 508, 23))
        self.progressBar.setProperty("value", 10)
        self.progressBar.setTextVisible(False)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))

	self.pic = QtGui.QLabel(self.topright)
	self.pic.setGeometry(10, 20, 300, 400)
	self.pic2 = QtGui.QLabel(self.topright)
	self.pic2.setGeometry(320, 20, 300, 400)

	self.hist = QtGui.QLabel(self.topleft)
	self.hist.setGeometry(200, 20, 300, 230)
	self.hist2 = QtGui.QLabel(self.topleft)
	self.hist2.setGeometry(200, 260, 300, 230)	
	
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
	self.fileText.setGeometry(108,10,500,40)

	self.inputfile = QtGui.QLabel(self.topright)
	self.inputfile.setGeometry(20,425,200,40)
	self.runingAlgo = QtGui.QLabel(self.topright)
	self.runingAlgo.setGeometry(620,7,200,40)
	self.runingAlgo.setText("Choose file")
	self.inputfile.setText("<font color='#0000c3' > <h3>INPUT IMAGE </h3></font>")
	self.outputfile = QtGui.QLabel(self.topright)
	self.outputfile.setGeometry(390,425,200,40)
	self.outputfile.setText("<font color='#0000c3' > <h3>OUTPUT IMAGE </h3></font>")

	

        openFile = QtGui.QAction(QtGui.QIcon('open.png'), 'Open', self.top)
        openFile.setShortcut('Ctrl+O')
        openFile.setStatusTip('Open new File')
        openFile.triggered.connect(self.showDialog)

	open2_btn = QtGui.QPushButton('Select GT Image', self.topleft)
	open2_btn.setStyleSheet('QPushButton {background-color: #A3C1DA; color: red;}')
        open2_btn.resize(180,30)
        open2_btn.move(10, 340)  
	open2_btn.clicked.connect(self.showDialog2)

	self.errorText = QtGui.QLabel(self.topleft)
	self.errorText.setGeometry(10,380,200,100)

	open2File = QtGui.QAction(QtGui.QIcon('open.png'), 'Select GT Image', self.topleft)
        open2File.setShortcut('Ctrl+O')
        open2File.setStatusTip('Open new File')
        open2File.triggered.connect(self.showDialog2)

        """menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(openFile)"""

        self.myLongTask = TaskThread()
        self.myLongTask.taskFinished.connect(self.onFinished)

	hbox.addWidget(self.splitter2)
		
      	self.setLayout(hbox)
      	QtGui.QApplication.setStyle(QtGui.QStyleFactory.create('Cleanlooks'))
		

        self.setGeometry(50, 50, 1200, 800)
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
	        pass
	    elif algo_index==6:
	        global K,iterNum
                K=int(self.returnAnswer1())
	        iterNum=int(self.returnAnswer2())
	    elif algo_index==7 :
	        global K,sigma
                K=int(self.returnAnswer1())
	        sigma=float(self.returnAnswer2()) 
	except:
	    self.runingAlgo.setText("<font color='red' > <h3>Error:Wrong Option </h3></font>")
	    return
	
	if img!="" :
            self.progressBar.setRange(0,0)
	    self.runingAlgo.setText("<font color='#97bf0d' > <h4> Running....</h4> </font>")
            self.myLongTask.start()
	else:
	    self.runingAlgo.setText("<font color='#0000c6' > <h4>No file choosen... </h4></font>")


    def onFinished(self):
        # Stop the pulsation
	self.runingAlgo.setText("<font color='#00ccff' > <h2> Done !</h2></font>")
        self.progressBar.setRange(0,1)
	pixmap = QtGui.QPixmap(os.getcwd()+"/test.jpg")
	pixmap3 = pixmap.scaled(300,300, QtCore.Qt.KeepAspectRatio)
	self.pic2.setPixmap(pixmap3)
	#histo_gram_start
	da=io.imread('test.jpg')
	data2=rgb2gray( da)
	hist, bins = np.histogram(data2, bins=50)
	width = 0.7 * (bins[1] - bins[0])
	center = (bins[:-1] + bins[1:]) / 2
	plt.bar(center, hist, align='center', width=width)
	plt.savefig("hist2.png")
	plt.close()
	del(data2)
	pixma = QtGui.QPixmap(os.getcwd()+"/hist2.png")
	pixma3 = pixma.scaled(300,200, QtCore.Qt.KeepAspectRatio)
	self.hist2.setPixmap(pixma3)
	global img,grd_img,file1,file2
	if grd_img!="":
	    data1=io.imread(os.getcwd()+"/test.jpg")
	    data2=io.imread(str(grd_img))
	    val=Err.err(data1,data2)
	    self.errorText.setText("<font color='#97bf0d' > <h4>GT Image :"+str(file2)+"<br><br> Output Image :"+str(file1)+"<br><br> Similarity Index :"+str(val)+"%</h4> </font>")    

	 

    def showDialog(self):
        self.fname = QtGui.QFileDialog.getOpenFileName(self, 'Open file', os.getcwd())
	global img
	img=self.fname
	data=io.imread(str(img))
	
	file1=img.split('/')[-1]
	layer=len(data.shape)
	if layer==1:
	    row=data.shape[0]
	    col=data.shape[1]
	    self.Img_inf.setText("<font color='#0000c3' ><h3> ANALYSIS </h3></font><font color='#97bf0d' ><h4>Image Name :"+str(file1)+"<br><br> Size : "+str(row)+" X "+str(col)+"<br><br> Type : One layer</h4></font>")
	if layer==3:
	    row=data.shape[0]
	    col=data.shape[1]
	    self.Img_inf.setText("<font color='#0000c3' ><h3> ANALYSIS </h3></font><font color='#97bf0d' ><<h4>Image Name :"+str(file1)+"<br><br> Size : "+str(row)+" X "+str(col)+"<br><br> Type : RGB Coloured</h4></font>")
	#histogram_start
	d=rgb2gray(data)
	hist, bins = np.histogram(d, bins=50)
	width = 0.7 * (bins[1] - bins[0])
	center = (bins[:-1] + bins[1:]) / 2
	plt.bar(center, hist, align='center', width=width)
	plt.savefig("hist.png")
	plt.close()
	pixma = QtGui.QPixmap("hist.png")
	pixma3 = pixma.scaled(300,200, QtCore.Qt.KeepAspectRatio)
	self.hist.setPixmap(pixma3)
	del(data)
        self.fileText.setText("<font color='#97bf0d' > <h5>"+str(img)+"</h5></font>")
	pixmap = QtGui.QPixmap(self.fname)
	pixmap3 = pixmap.scaled(300,300, QtCore.Qt.KeepAspectRatio)
	self.pic.setPixmap(pixmap3)

    def showDialog2(self):
        self.fname = QtGui.QFileDialog.getOpenFileName(self, 'Open file', os.getcwd())
	global grd_img,img,file1,file2
	grd_img=self.fname
        print grd_img,img,file1,file2
	if img !="":
	    file1=img.split('/')[-1]
	file2=grd_img.split('/')[-1]
	self.errorText.setText("<font color='#97bf0d' > <h4>GT Image :"+str(file2)+"<br><br> Output Image :"+str(file1)+"</h4> </font>")

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
                self.DisText.setText("<font color='blue' > <h1> K-mean Algorithm </h1></font><font color='#97bf0d' > <h3>This algorithm uses to find K cluster in image. For which <br/> you have to select K value and Iteration value .If you <br> have no idea than select K = 5 and iterarion no more then<br> 10.<br></h3></font>")
	elif b.text() == "Global Thresholding":
	    if b.isChecked() == True:
		global algo_index
		algo_index=2
		self.var1.setText("<font color='#97bf0d' > <h4>N value :</h4></font>")
		self.var2.setText("<font color='#97bf0d' > <h4>Delta Value :</h4></font>")
		self.var3.setText("<font color='#97bf0d' > <h4>variable3 :</h4></font>")
                self.DisText.setText("<font color='blue' > <h1> Global Thresholding </h1></font><font color='#97bf0d' > <h3>This algorithm uses to find the threshold values so that<br> we can divide the image in N part ( Generally in Two part<br> Foreground / Background ).Here you have to select N <br> and delta, If you have no idea select N=2 and delta = 30.<br> </h3></font>")
	elif b.text() == "Regin Grow Method":
	    if b.isChecked() == True:
		global algo_index
		algo_index=3
		self.var1.setText("<font color='#97bf0d' > <h4>Row Value :</h4></font>")
		self.var2.setText("<font color='#97bf0d' > <h4>Col Value :</h4></font>")
		self.var3.setText("<font color='#97bf0d' > <h4>Threshold :</h4></font>")
                self.DisText.setText("<font color='blue' > <h1> Regin Grow Method </h1></font><font color='#97bf0d' > <h3>This algorithm generally uses to find associated region <br>for given seeds ( points ). For this you have to select <br>seeds point (row ,col ) and threshold. If you have no idea,<br> Select threshold = 40.  <br></h3></font>")
	elif b.text() == "Graph Based Method":
	    if b.isChecked() == True:
		global algo_index
		algo_index=4
		self.var1.setText("<font color='#97bf0d' > <h4>Sigma Value :</h4></font>")
		self.var2.setText("<font color='#97bf0d' > <h4>K Value :</h4></font>")
		self.var3.setText("<font color='#97bf0d' > <h4>MinSize :</h4></font>")
                self.DisText.setText("<font color='blue' > <h1> Graph Based Method </h1></font><font color='#97bf0d' > <h3>This algorithm use the value of a threshold to merge <br>different components to produce a segmented image.<br>It takes a minsize variable for merging very small size <br>components.If you have no idea, Select sigma = 0 and <br>minsize = 20 and K = 500.<br></h3></font>")
	elif b.text() == "Otsu Method":
	    if b.isChecked() == True:
		global algo_index
		algo_index=5
		self.var1.setText("<font color='#97bf0d' > <h4>Variable1 :</h4></font>")
		self.var2.setText("<font color='#97bf0d' > <h4>Variable2 :</h4></font>")
		self.var3.setText("<font color='#97bf0d' > <h4>Variable3 :</h4></font>")
                self.DisText.setText("<font color='blue' > <h1> Otsu Method </h1></font><font color='#97bf0d' > <h3>This algorithm uses to find the threshold values so that<br> we can divide the image in two part Foreground and <br> Background .<br><br><br> </h3></font>")
	elif b.text() == "Watershed Method":
	    if b.isChecked() == True:
		global algo_index
		algo_index=6
		self.var1.setText("<font color='#97bf0d' > <h4>Variable1 :</h4></font>")
		self.var2.setText("<font color='#97bf0d' > <h4>Variable2 :</h4></font>")
		self.var3.setText("<font color='#97bf0d' > <h4>Variable3 :</h4></font>")
                self.DisText.setText("<font color='blue' > <h1> Watershed Method </h1></font><font color='#97bf0d' > <h3>There are some information about this algorithm like<br/> K value needed or something else</h3></font>")
        elif b.text() == "Fuzzy C-Mean":
	    if b.isChecked() == True:
		global algo_index
		algo_index=7
		self.var1.setText("<font color='#97bf0d' > <h4>C value :</h4></font>")
		self.var2.setText("<font color='#97bf0d' > <h4>sigma :</h4></font>")
		self.var3.setText("<font color='#97bf0d' > <h4>Variable3 :</h4></font>")
                self.DisText.setText("<font color='blue' > <h1> Fuzzy C-Mean  </h1></font><font color='#97bf0d' > <h3>This algorithm uses to find C cluster in image on basis <br>of probability. For which you have to select C value <br>and sigma. If you have no idea than select C = 5 and<br> sigma = 0.3<br>.</font>")
      
	

class TaskThread(QtCore.QThread):
    taskFinished = QtCore.pyqtSignal()
    def run(self):
	global img,algo_index
	li=img.split('/')     
        file1=li[len(li)-1] 
	data=io.imread(str(img))
	
	if algo_index==1:
	    global K,iterNum
	    data=Kmean.kmean(data,iterNum,K)
	elif algo_index==2:
	    global Num_par,delta
	    data=GlobalThresholding.global_threshold(data,Num_par,delta)
	elif algo_index==3:
	    global row,col,thre
	    data=Region_grow.region_grow_priorityQ(data,[row,col],thre)
	elif algo_index==4:
	    global sigma,mean_size,K_graph
	    print K_graph
	    data=graph_based.graph_based_seg(data,mean_size,K_graph,sigma)
	elif algo_index==5:
	    data=otsu.otsu(data)
	elif algo_index==6:
	    global K,iterNum
	    data=Kmean.kmean(data,iterNum,K)
	elif algo_index==7:
	    global K,sigma
	    data=fuzzy.fuzzy(data,K,sigma)
	im = Image.fromarray(data)
	im.save(os.getcwd()+"/test.jpg")
        self.taskFinished.emit()  

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    ui = Ui_Form()
 
    ui.show()
    sys.exit(app.exec_())
