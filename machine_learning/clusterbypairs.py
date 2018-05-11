import os,sys
import numpy as np

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

os.system("./release04_0.55 "+sys.argv[1])
imglist=os.popen("awk '{print $1}' "+sys.argv[1]).read().splitlines()#[:-1]
num=len(imglist)
lines=os.popen("cat output_file*").read()
mat = np.fromstring(lines,"f",-1," ").reshape(-1,3)

index1=mat[:,0].astype("int32")
index2=mat[:,1].astype("int32")
dists=mat[:,2].astype("f")

labels,rank=makesameSet(num)

################
threshold=0.7
wh=np.where(dists>threshold)
for i in wh[0]:
    unionsameSet(index1[i] , index2[i] , labels , rank)

for i in range(num):
    findsame(i,labels)

out=open("labels_0.7","w")
for i in range(num):
    print >>out,imglist[i],labels[i]

out.close()
