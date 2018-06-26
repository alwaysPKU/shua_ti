import os,sys
import numpy as np
import datetime


def get_time():
    return datetime.datetime.now()

def makesameSet( size):

    samerank=[0]*size
    same=[i for i in range(size)]
    return same,samerank
def findsame(x,same):

    if x != same[x]:
        same[x] = findsame(same[x],same)
    return same[x]

def unionsameSet( x,y,same,samerank):
    x = findsame(x,same)
    y = findsame(y,same)
    if x == y :
        return
    if samerank[x] > samerank[y]:
        same[y] = x
        
    else:
        same[x] = y

        if samerank[x] == samerank[y]:
            samerank[y]+=1
#t1=get_time()
#print 'start compute dist:',t1
#os.system("./release04_0.7 "+sys.argv[1])
#t2=get_time()
#print 'end compute dist:',t2,t2-t1
#imglist=os.popen("awk '{print $1}' "+sys.argv[1]).read().splitlines()#[:-1]
#num=len(imglist)
#lines=os.popen("cat output_file*").read()
#mat = np.fromstring(lines,"f",-1," ").reshape(-1,3)
#t3=get_time()
#print 'end load dist:',t3,t3-t2
#index1=mat[:,0].astype("int32")
#index2=mat[:,1].astype("int32")
#dists=mat[:,2].astype("f")
def cluster(mat,num):
    index1=mat[:,0].astype("int32")
    index2=mat[:,1].astype("int32")
    dists=mat[:,2].astype("f")
    labels,rank=makesameSet(num)

    #threshold=0.7
    #wh=np.where(dists>threshold)
    #for i in wh[0]:
    for i in range(mat.shape[0]):
        unionsameSet(index1[i] , index2[i] , labels , rank)

    for i in range(num):
        findsame(i,labels)

    print 'end 1 cluster:'
    #out=open(sys.argv[2],"w")
    #for i in range(num):
    #    print >>out,imglist[i],labels[i]
    return labels
   # out.close()
   # t5=get_time()
   # print 'end write labels:',t5,t5-t4
