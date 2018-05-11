import os,sys
import numpy as np
from ctypes import *
import multiprocessing
from sklearn.preprocessing import normalize


#topk=1
maxappearance=4
filter_threshold=0.9
topN=1000
dim=384
GPUs=[0,1,2]
KEEP_FIRST=False
calc= CDLL('./libthreshold.so')
calc.calcthreshold.argtypes = [POINTER(c_float),POINTER(c_float) ,POINTER(c_int),c_float,POINTER(c_int) ,POINTER(c_int) ,POINTER(c_float) ]


def read(f):

    npfile=np.load(f)
    imgs=npfile["imgs"]
    mat=npfile["features"]  
    keep=range(len(imgs))
    if KEEP_FIRST:
        dic={}
        keep=[]
        cnt=0
        for img in imgs:
            if not dic.has_key(img):
                dic[img]=1
                keep.append(cnt)
        
            cnt+=1
    print len(imgs),"imgs in all",len(keep),"imgs left"
       
    return imgs[keep],normalize(mat[keep])

def scoremapping(score):
    return np.maximum(np.minimum(1.4084507*(1+score)/2-0.17746479,0.9999),0)



def unmap(score):
    return (score+0.17746479)*2/1.4084507-1

def do(query,gallery,lq,lg,dim,topk,index,score,gpu):
    ranker.matrixMulTopK(query.ctypes.data_as(POINTER(c_float)),
    gallery.ctypes.data_as(POINTER(c_float)),
    lq,lg,dim,topk,
    index.ctypes.data_as(POINTER(c_int)),
    score.ctypes.data_as(POINTER(c_float)),
    gpu
    )
    return list(index),list(score)




def do2(query,gallery,lq,lg,dim,threshold,shift,gpu):
    k=10**8
    index1=np.zeros(k,dtype="int32")
    index2=np.zeros(k,dtype="int32")
    scores=np.zeros(k,dtype="float32")
    cnt=0
    paras=np.array([lq,lg,dim,shift,cnt,k,gpu],dtype="int32")
    calc.calcthreshold(
    query.ctypes.data_as(POINTER(c_float)),
    gallery.ctypes.data_as(POINTER(c_float)),
    paras.ctypes.data_as(POINTER(c_int)),float(threshold),
    index1.ctypes.data_as(POINTER(c_int)),
    index2.ctypes.data_as(POINTER(c_int)),
    scores.ctypes.data_as(POINTER(c_float)))
    assert(paras[4]<=k)
   
    return zip(index1[:paras[4]],index2[:paras[4]],scoremapping(scores[:paras[4]]))


def run(qmat,gmat,threshold):
    
#    index=np.zeros(len(qmat)*topk,"i")
#    score=np.zeros(len(qmat)*topk,"f")

    Query=qmat.reshape(-1)
    Gallery=gmat.reshape(-1)
       
    length=len(qmat)
    assert(len(gmat)<400000)
    num=100
    threshold=unmap(threshold)
    ans=[]   
    pool=multiprocessing.Pool(processes=3)
   
    for i in range(num):
        ans.append(pool.apply_async(
#        apply(
        do2,(
        Query[length*i/num*dim:length*(i+1)/num*dim], 
        Gallery, 
        length*(i+1)/num-length*i/num, len(gmat), dim, threshold,length*i/num,
        GPUs[i%3])
        )
        )

    pool.close()
    pool.join()
    tuples=[]
    for a in ans:
        ret=a.get()
        tuples.extend(ret)
    return np.array(tuples)


def printresults(qimgs,gimgs,tuples,topN,output):
    out=open(output,"w")
    gdic={}
    qdic={}
    blq=[]
    blg=[]
    for t in tuples:
        if not qdic.has_key(t[0]):
            qdic[t[0]]=0
        if not gdic.has_key(t[1]):
            gdic[t[1]]=0
        gdic[t[1]]+=1
        qdic[t[0]]+=1
        if gdic[t[1]]>=maxappearance:
            blg.append(t[1])
        if qdic[t[0]]>=maxappearance:
            blq.append(t[0])
    ans=[]
    for t in tuples:
        if t[0] in blq or t[1] in blg:
            continue
        else:
            ans.append(t)
    print "before",len(tuples),"after",len(ans)

    i=0
    cnt=0
    dic={}
    ans.sort(key=lambda x:-x[2])
    while cnt<topN and i<len(tuples)-1:
        a=int(ans[i][0])
        b=int(ans[i][1])
#        print a,b,ans[i][2]
        if not dic.has_key(a):
            cnt+=1
            dic[a]=1
            print >>out,qimgs[a],gimgs[b],ans[i][2]
        i+=1
    if  cnt<topN :
        print "not enough valid pairs"
    out.close()
    

def main(query,gallery):

    qimgs,qmat=read(query)
    gimgs,gmat=read(gallery)
    fn="results"+str(filter_threshold)+".npy"
    if not os.path.exists(fn):
        tuples=run(qmat,gmat,filter_threshold)
        np.save(fn,tuples)
    else:
        tuples=np.load(fn)

    printresults(qimgs,gimgs,tuples,topN,"output.txt")
    



if __name__ == "__main__":
    main(sys.argv[1],sys.argv[2])
