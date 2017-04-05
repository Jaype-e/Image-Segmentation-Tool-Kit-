import numpy as np
import sys
import matplotlib.pyplot as plt
from skimage import io
from numpy import abs

def fuzzy(data,k,sigma):
	row=data.shape[0]
	col=data.shape[1]
	m=row*col
	layer=1
	if len(data.shape)==3:
		layer=3
	data=data.reshape(m,layer)
	u=np.zeros((m,k))
	for i in xrange(m):
		u[i][np.random.randint(0,k-1)]=1
	y=2
	#print u
	print " Answer should be " ,m*k
	for kk in xrange(5) :
		c=[ [ 0.0 for t in xrange(layer) ] for j in xrange(k)]
		for i in xrange(k):
			sum1=0.0
			for j in xrange(m):
				for t in xrange(layer):
					c[i][t]+=u[j][i]*u[j][i]*data[j][t]
				sum1=sum1+u[j][i]*u[j][i]
			for t in xrange(layer):	
				if c[i][t]!=0:	
					c[i][t]=c[i][t]/sum1
		ans=0	
		for i in xrange(m):
			sum1=0.0
			for j in xrange(k):
				p=0.0
				for t in xrange(layer):
					p+=(data[i][t]-c[j][t])*(data[i][t]-c[j][t])

				sum1+=1.0/( p )
			for j in xrange(k):
				p=0.0000001
				for t in xrange(layer):
					p+=(data[i][t]-c[j][t])*(data[i][t]-c[j][t])
				p=1.0/( sum1*p )
				if abs( u[i][j]-p ) <= sigma:
					ans=ans+1
				u[i][j]=p
		print ans		
		if ans == m*k:
			break
	avg=[ [ 0.0 for t in xrange(layer) ] for j in xrange(k)]
	idx=[0 for t in xrange(m)]	
	fre=[0 for y in xrange(k) ]
	y=0	
	print type(u)
	for i in xrange(m):
		y=0
		tmp=0.0
		for x in xrange(k):
			if tmp < u[i][x]:
				tmp=u[i][x]
				y=x
		idx[i]=y
		fre[y]=fre[y]+1
		for t in xrange(layer):
			avg[y][t]+=data[i][t]
	for i in xrange(k):
		for t in xrange(layer):
			avg[i][t]=avg[i][t]/fre[i] 
	for i in xrange(m):
		for t in xrange(layer):
			data[i][t]=avg[idx[i]][t]				


	data=data.reshape(row,col,layer)		
	return data    



