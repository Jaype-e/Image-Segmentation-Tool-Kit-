import numpy as np
import sys
import matplotlib.pyplot as plt
from skimage import io
import Queue

def dist( a,b,thre):
	if (abs(a[0]-b[0]) >thre ) or (abs(a[1]-b[1]) >thre ) or (abs(a[2]-b[2]) >thre ):
		return False
	return True

def dist1( a,b):
	return ( abs(a[0]-b[0])+abs(a[1]-b[1])+abs(a[2]-b[2]) )

def region_grow_point(data,seed,thre):
	row=data.shape[0]
	col=data.shape[1]
	Cluster=np.zeros((row,col,3),dtype=float)
	visited=[ [ False for i in xrange(col)] for j in xrange(row) ] 
	q=Queue.Queue()
	q.put(seed)
	direction=[ (1,0),(-1,0),(0,1),(0,-1) ]
	point=seed
	#data[seed[0]][seed[1]]=[0,0,0]
	while not q.empty() :
		temp=q.get()
		#print temp
		if visited[temp[0]][temp[1]]==False:
			visited[temp[0]][temp[1]]=True
			for j in direction:
				if ( 0<temp[0]+j[0]<row ) and ( 0<temp[1]+j[1]<col ):
					cur_point=(temp[0]+j[0],temp[1]+j[1])
					#print dist(data[ cur_point[0] ][ cur_point[1] ],data[point[0]][point[1]],thre)
					if dist(data[ cur_point[0] ][ cur_point[1] ],data[point[0]][point[1]], thre) :
						q.put( (cur_point[0],cur_point[1]) )
						Cluster[ cur_point[0] ][ cur_point[1] ]=[255,0,0]
						
	for i in xrange(row):
		for j in xrange(col):
			if Cluster[i][j].any()!=0:
				data[i][j]=Cluster[i][j]

	for j in xrange(col):				
		data[seed[0]][j]=[0,0,0]
	for j in xrange(row):
		data[j][seed[1]]=[0,0,0]	

	return data			

def region_grow_avg(data,seed,thre):
	row=data.shape[0]
	col=data.shape[1]
	Cluster=np.zeros((row,col,3),dtype=float)
	visited=[ [ False for i in xrange(col)] for j in xrange(row) ] 
	q=Queue.Queue()
	q.put(seed)
	direction=[ (1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1) ]
	point=map(float,data[ seed[0] ][ seed[1]])
	size=1;
	while not q.empty() :
		temp=q.get()
		#print temp
		if visited[temp[0]][temp[1]]==False:
			visited[temp[0]][temp[1]]=True
			for j in direction:
				if ( 0<temp[0]+j[0]<row ) and ( 0<temp[1]+j[1]<col ):
					cur_point=(temp[0]+j[0],temp[1]+j[1])
					#print point,size
					if dist1(data[ cur_point[0] ][ cur_point[1] ],point)<=thre  :
						point= ( point*size+data[ cur_point[0] ][ cur_point[1] ] )/(size+1)
						size=size+1
						q.put( (cur_point[0],cur_point[1]) )
						Cluster[ cur_point[0] ][ cur_point[1] ]=[255,0,0]
						
	for i in xrange(row):
		for j in xrange(col):
			if Cluster[i][j].any()!=0:
				data[i][j]=Cluster[i][j]

	for j in xrange(col):				
		data[seed[0]][j]=[0,0,0]

	for j in xrange(row):
		data[j][seed[1]]=[0,0,0]	

	return data

def region_grow_priorityQ(data,seed,thre):
	row=data.shape[0]
	col=data.shape[1]
	Cluster=np.zeros((row,col,3),dtype=float)
	visited=[ [ False for i in xrange(col)] for j in xrange(row) ] 
	q=Queue.PriorityQueue()
	q.put((0,seed[0],seed[1]))
	direction=[ (1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1) ]
	mean=map(float,data[ seed[0] ][ seed[1]])
	size=1;
	while not q.empty() :
		temp=q.get()
		#print temp
		if visited[temp[1]][temp[2]]==False:
			visited[temp[1]][temp[2]]=True
			mean= ( mean*size + data[ temp[1] ][ temp[2] ] )/(size+1)
			size=size+1
			for j in direction:
				if ( 0<temp[1]+j[0]<row ) and ( 0<temp[2]+j[1]<col ):
					cur_point=(temp[1]+j[0],temp[2]+j[1])
					dis=dist1(data[ cur_point[0] ][ cur_point[1] ],mean)
					if dis<=thre :
						q.put( (dis,cur_point[0],cur_point[1]) )
						Cluster[ cur_point[0] ][ cur_point[1] ]=[255,0,0]
						
	for i in xrange(row):
		for j in xrange(col):
			if Cluster[i][j].any()!=0:
				data[i][j]=Cluster[i][j]

	for j in xrange(col):				
		data[seed[0]][j]=[0,0,0]

	for j in xrange(row):
		data[j][seed[1]]=[0,0,0]	

	return data	

"""data=io.imread("bird_small.png")
layer=1
print "k-mean run"
row=data.shape[0]
col=data.shape[1]

if len(data.shape)==3:
	layer=data.shape[2]

data=region_grow(data,[50,25],60)
plt.imshow(data)
plt.show()"""	

