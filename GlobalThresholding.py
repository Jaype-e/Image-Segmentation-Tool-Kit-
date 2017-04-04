import numpy as np
import sys
import matplotlib.pyplot as plt
from skimage import io
from numpy import abs


def global_threshold(data,n)
	layer=1
	row=data.shape[0]
	col=data.shape[1]
	m=row*col

	if len(data.shape)==3:
		layer=data.shape[2]

	gray_layer=np.zeros((row,col),dtype=float)

	for i in xrange(row):
		for j in xrange(col):
			gray_layer[i][j]=0.299*data[i][j][0]+0.587*data[i][j][1]+0.114*data[i][j][2]

	gray_layer=gray_layer.reshape( m,1 )
	delta=30
	cur_mean=np.mean(gray_layer)
	 # number of thresholds
	n_minus=0
	while True :
		l=[]
		for j in xrange(n):
			l.append([])
		k=[0]
		for j in xrange(1,n):
			k.append((j*2.0*cur_mean)/n)
		k.append(256)
		for i in xrange(m):
			for j in xrange(n):
				if k[j] <= gray_layer[i] and gray_layer[i] <k[j+1] :
					l[j].append(gray_layer[i])
					break
		mean_tem=[]
		n_minus=0
		for j in xrange(n):
			if len(l[j])!=0:
				mean_tem.append( np.mean(l[j]) )
			else:
				n_minus=n_minus+1;
		
		mean_temp_np=np.array(mean_tem)
		tem_mean=np.mean(mean_temp_np)

		if abs(cur_mean-tem_mean)< delta:
			break
		cur_mean=tem_mean
		del(mean_tem)
		del(l)
		del(k)

	k=[0]
	n_color=[0]
	for j in xrange(1,n):
		k.append((j*2.0*cur_mean)/n)
		n_color.append(0)	
	k.append(256)
	gray_layer=gray_layer.reshape( row,col )
	avg=256.0/n
	for i in xrange(row):
		for j in xrange(col):
			for t in xrange(n):
				if k[t] <= gray_layer[i][j] and gray_layer[i][j] <k[t+1] :
					data[i][j][0]=data[i][j][1]=data[i][j][2]=(t*avg)
					n_color[t]=n_color[t]+1
					#gray_layer[i][j]=t*avg
					
			
	for j in xrange(n):
		print k[j],n_color[j]
	print "n =",n-n_minus
	return data
	






