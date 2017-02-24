import numpy as np
import sys
import matplotlib.pyplot as plt
from skimage import io

if len(sys.argv) < 2:
	print("Enter the model option.")
	exit()

filename=sys.argv[1]
k=16
if len(sys.argv)==3:
	k=int(sys.argv[2])

def find_cluster(data,idx,k):
    m=data.shape[0]
    n=data.shape[1]
    idx_count=[0 for i in range(k)]
    cluster_sum=np.zeros((k,n),dtype=float)
    for i in xrange(m):
        for j in xrange(n):
            cluster_sum[idx[i]][j]+=data[i][j]
        idx_count[idx[i]]+=1    
    for i in xrange(k):
        for j in xrange(n):
            if idx_count[i]>0:
                cluster_sum[i][j]=cluster_sum[i][j]/idx_count[i]
    #print cluster_sum        
    return cluster_sum        
    

def Kmean(Cluster,data,idx):
    k=Cluster.shape[0]
    m=data.shape[0]
    n=data.shape[1]
    for i in range(m):
        cur_dis=0.0
        for p in range(n):
            cur_dis+=(Cluster[0][p]-data[i][p])**2    
        idx[i]=0    
        for j in range(k):
            temp_dis=0.0
            for p in range(n):
                temp_dis+=(Cluster[j][p]-data[i][p])**2
            if temp_dis<cur_dis:
                idx[i]=j
                cur_dis=temp_dis
    #print idx
    Cluster=find_cluster(data,idx,k)
    return Cluster

def runKmean(data,ite,k,Binery):
    m=data.shape[0]
    randomPerm=np.random.permutation(m)
    Cluster=np.zeros((k,3),dtype=float)
    for i in range(k):
        Cluster[i,:]=data[randomPerm[i],:]
        
    idx=range(m)
    for h in xrange(ite):
        print "k-mean running iter",h
        Cluster=Kmean(Cluster,data,idx)
    for i in range(m):
        data[i,:]=Cluster[idx[i],:]

    if Binery==True :
	if Cluster[0][0]*Cluster[0][1]*Cluster[0][2] > Cluster[1][0]*Cluster[1][1]*Cluster[1][2] :
            Cluster[0,:]=[255,255,255]
	    Cluster[1,:]=[0,0,0]
	else :
            Cluster[0,:]=[0,0,0]
	    Cluster[1,:]=[255,255,255] 

    for i in range(m):
        data[i,:]=Cluster[idx[i],:]
       
    return data    
    
    
#start of main

data=io.imread(filename)
layer=1
print "k-mean run"
row=data.shape[0]
col=data.shape[1]

if len(data.shape)==3:
	layer=data.shape[2]

m=row*col
data=data.reshape(m,layer)
k=16
if len(sys.argv)>=3:
	k=int(sys.argv[2])

print "data shapes: ",data.shape[0],data.shape[1]

Binery=False

if len(sys.argv)==4:
	Binery=bool(sys.argv[3])

print k
data=runKmean(data,10,k,Binery)

data=data.reshape(row,col,layer)
plt.imshow(data)
plt.show()

