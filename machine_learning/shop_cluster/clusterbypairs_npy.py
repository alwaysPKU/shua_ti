import os,sys
import numpy as np
import datetime

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

#os.system("./release04_0.55 "+sys.argv[1])
imglist=os.popen("awk '{print $1}' "+sys.argv[1]).read().splitlines()#[:-1]
num=len(imglist)
#lines=os.popen("cat output_file*").read()
#mat = np.fromstring(lines,"f",-1," ").reshape(-1,3)
t1 = datetime.datetime.now()
file = sys.argv[2]
print 'input', file
mat = np.load(file)
print 'mat shape:', mat.shape
t2 = datetime.datetime.now()
print 'end load dist:', t2-t1
index1=mat[:,0].astype("int32")
index2=mat[:,1].astype("int32")
dists=mat[:,2].astype("f")

labels,rank=makesameSet(num)

################
threshold=0.68
wh=np.where(dists>threshold)
for i in wh[0]:
    unionsameSet(index1[i] , index2[i] , labels , rank)

for i in range(num):
    findsame(i,labels)
t3 = datetime.datetime.now()
print 'end first cluster:', t3-t2
output_file = 'labels_'+str(threshold)+'_npy'
print 'out_put:', output_file
out=open(output_file,"w")
for i in range(num):
    print >>out,imglist[i],labels[i]

out.close()
print 'end write:', datetime.datetime.now()-t3
