import numpy as np
import sys
import matplotlib.pyplot as plt
from skimage import io
from graph import build_graph, segment_graph
from smooth_filter import gaussian_grid, filter_image
from random import randint

def initl( idx, qrank,maxMST,n):
	for i in range(0,n):
		idx.append(i);
		qrank.append(1);
		maxMST.append(0)
#Disjoint_Set_Union
def findparent(idx, u):
    if (idx[u]==u):
        return u
    idx[u]=findparent(idx,idx[u]); #Path Compression
    return idx[u];
    
def qunion(idx,qrank,maxMST,w,u,v):
    p1=findparent(idx,u);
    p2=findparent(idx,v);
    if (p1==p2):
        return ;
    elif(qrank[p1]<=qrank[p2]):
		idx[p1]=p2;qrank[p2]+=qrank[p1];
		maxMST[p2]=w 
    else:
		idx[p2]=p1;qrank[p1]+=qrank[p2]; 
		maxMST[p1]=w

def isconnected( idx, u, v):
    p1=findparent(idx,u);
    p2=findparent(idx,v);
    if (p1==p2):
        return True;
    else:
        return False;
      
#Building-4-connected-graph
def compute_edges(edges,data,row,col,layer):
	for i in range(0,row):
		for j in range(0,col):
			weight=0
			if i==0 and j!=0:
				for p in range(0,layer):
					weight+=(int(data[i][j][p])-int(data[i][j-1][p]))**2
				edges.append([weight,j,j-1])
			elif i!=0 and j==0:
				for p in range(0,layer):
					weight+=(int(data[i][j][p])-int(data[i-1][j][p]))**2
				edges.append([weight,col*i,col*(max(0,i-1)) ])
			elif i!=0 and j!=0:
				for p in range(0,layer):
					weight+=(int(data[i][j][p])-int(data[i-1][j][p]))**2
				edges.append([weight,col*(i)+j,col*(max(0,i-1))+j ])
				weight=0
				for p in range(0,layer):
					weight+=(int(data[i][j][p])-int(data[i][j-1][p]))**2
				edges.append([weight,col*(i)+j,col*(i)+j-1 ])
					
#computing_segmented_image				
def graph_based(data,k,m,edges,idx,qrank,maxMST,minsize): 
   	n=len(edges)
   	count=0
   	for i in range(0,n):
		if isconnected(idx,edges[i][1],edges[i][2])==False:
			p1=findparent(idx,edges[i][1])
			p2=findparent(idx,edges[i][2])
			t1=maxMST[p1] + ( k/qrank[p1] )
			t2=maxMST[p2] + ( k/qrank[p2] )
			if edges[i][0]<min(t1,t2):
				count+=1
				qunion(idx,qrank,maxMST,edges[i][0],edges[i][1],edges[i][2])
	print count,n
	for i in range(0,n):
		p1=findparent(idx,edges[i][1])
		p2=findparent(idx,edges[i][2])
		if p1!=p2:
			if qrank[p1]<minsize or qrank[p2]<minsize:
				qunion(idx,qrank,maxMST,edges[i][0],edges[i][1],edges[i][2])
	for i in range(0,m):
		idx[i]=findparent(idx,i)
	idxset=idx
	idxset=set(idxset);idxset=list(idxset);nset=len(idxset)
	maps1=dict();maps2=dict();maps3=dict();maps4=dict();
	print "no of regions found",nset
	for i in range(0,nset):
		maps1[idxset[i]]=0
		maps2[idxset[i]]=0
		maps3[idxset[i]]=0
		maps4[idxset[i]]=0
	for i in range(0,m):
		maps1[idx[i]]+=data[i][0]
		maps2[idx[i]]+=data[i][1]
		maps3[idx[i]]+=data[i][2]
		maps4[idx[i]]+=1
	for i in range(0,m):
		data[i][0]=maps1[idx[i]]/maps4[idx[i]]
		data[i][1]=maps2[idx[i]]/maps4[idx[i]]
		data[i][2]=maps3[idx[i]]/maps4[idx[i]]	
	return data
	
def graph_based_seg(data,minsize,k,sigma):
	m=int();idx=list();qrank=list();edges=list();maxMST=list()
	layer=1
	print "Graph_based run"
	row=data.shape[0]
	col=data.shape[1]
	if len(data.shape)==3:
		layer=data.shape[2]
	m=row*col
	#Applying_Gaussian_Filter
	
	data=data.reshape(m,layer)
	r=data[:,0];r=r.reshape(m,1)
	g=data[:,1];g=g.reshape(m,1)
	b=data[:,2];b=b.reshape(m,1)
	
	grid = gaussian_grid(sigma)
	r=filter_image(r,grid);r=r.reshape(1,m)
    	g=filter_image(g,grid);g=g.reshape(1,m)
    	b=filter_image(b,grid);b=b.reshape(1,m)
    	data[:,0]=r
	data[:,1]=g
	data[:,2]=b
	data=data.reshape(row,col,layer)
	
	initl(idx,qrank,maxMST,m)
	compute_edges(edges,data,row,col,layer)
	edges.sort()
	data=data.reshape(m,layer)
	
	data=graph_based(data,k,m,edges,idx,qrank,maxMST,minsize)#segmentating
	data=data.reshape(row,col,layer)
	
	return data 
