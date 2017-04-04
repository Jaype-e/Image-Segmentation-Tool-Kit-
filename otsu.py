import numpy as np
from numpy import abs
from matplotlib import pyplot as plt
import sys
from skimage import io

def otsu(data):
	
	hist=[ 0 for j in xrange(256) ]
	layer=1
	row=data.shape[0]
	col=data.shape[1]

	if len(data.shape)==3:
		layer=data.shape[2]

	gray_layer=np.zeros((row,col),dtype=int)

	for i in xrange(row):
		for j in xrange(col):
			gray_layer[i][j]=0.299*data[i][j][0]+0.587*data[i][j][1]+0.114*data[i][j][2]

	for i in xrange(row):
		for j in xrange(col):
			hist[gray_layer[i][j]]=hist[gray_layer[i][j]]+1
	total=0
	ut=0.0
	for i in hist:
		total+=i
	p=[]
	for i in hist:
		p.append((i*1.00)/total)

	for i in xrange(0,256):
		ut+=i*p[i]

	threshold=0.0
	sigma=0.0
	w0=0.0
	w1=0.0
	sum1=0
	for i in xrange(0,255):
		w0+=p[i]
		if w0==0:
			continue

		w1=1-w0
		if w1==0:
			break	
		sum1+=i*p[i]
		
		u0=sum1/w0
		u1=(ut-sum1)/w1	
		sigmab=w0*w1*(u0-u1)*(u0-u1)

		if sigmab > sigma:
			sigma=sigmab
			threshold=i
		#print threshold	

	print threshold					
	for i in xrange(row):
		for j in xrange(col):
			if gray_layer[i][j]>threshold:
				data[i][j][0]=data[i][j][1]=data[i][j][2]=255
			else:
				data[i][j][0]=data[i][j][1]=data[i][j][2]=0
				
	return data

data = io.imread('disha.png')
data=otsu(data)
plt.imshow(data)
plt.show()




