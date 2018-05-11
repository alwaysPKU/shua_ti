import os,sys
import numpy as np


def add(dic,key,v):
    if not dic.has_key(key):
        dic[key]=0
    dic[key]+=1

def check(tuples):
   
#    print "################"
#    print "fname=",f
    print tuples.shape[0]," pairs in total"
    print len(set(tuples[:,0])),"query images concerned"
    print len(set(tuples[:,1])),"gallery images concerned"

    gdic={}
    qdic={}
    for t in tuples:      
       add(qdic,t[0],1)
       add(gdic,t[1],1)

    qnum=np.array(qdic.values())
    gnum=np.array(gdic.values())
    for i in [1,2,3,4]:
        print "size =",i,"query",np.sum(qnum==i),"gallery",np.sum(gnum==i)
    print "size >=5","query",np.sum(qnum>=5),"gallery",np.sum(gnum>=5)
    



    print ""

def check2(f):
    tuples=np.load(f)
    gdic={}
    qdic={}
    
    for t in tuples:
        if not qdic.has_key(t[0]):
            qdic[t[0]]=0
        if not gdic.has_key(t[1]):
            gdic[t[1]]=0
        gdic[t[1]]+=1
        qdic[t[0]]+=1
    for maxappearance in [2,3,4,5]:
        blq=[]
        blg=[]
        print "maxappearance=",maxappearance
        for t in tuples:
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
        check(np.array(ans))


files=os.popen("ls|grep results*npy").readlines()
for f in files:
    check2(f[:-1])
