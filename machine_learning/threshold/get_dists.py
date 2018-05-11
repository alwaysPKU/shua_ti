import os,sys
import numpy as np
from ctypes import *
import multiprocessing
from sklearn.preprocessing import normalize
import datetime


#topk=1
maxappearance=4
filter_threshold= -1
topN=1000
dim=384
GPUs=[0,1,2]
KEEP_FIRST=False
calc= CDLL('./libthreshold.so')
calc.calcthreshold.argtypes = [POINTER(c_float),POINTER(c_float) ,POINTER(c_int),c_float,POINTER(c_int) ,POINTER(c_int) ,POINTER(c_float) ]


def read(f):
    mat = np.array(np.loadtxt(f, usecols=range(1,385)), 'f')
    return normalize(mat)


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
   
    # return zip(index1[:paras[4]],index2[:paras[4]],scoremapping(scores[:paras[4]]))
    return zip(index1[:paras[4]], index2[:paras[4]], scores[:paras[4]])


def run(qmat,threshold):
    Query=qmat.reshape(-1)
    Gallery=Query
       
    length=len(qmat)
   # assert(len(qmat)<400000)
    num=100
    # threshold=unmap(threshold)
    ans=[]   
    pool=multiprocessing.Pool(processes=3)
   
    for i in range(num):
        ans.append(pool.apply_async(
        do2,(
        Query[length*i/num*dim:length*(i+1)/num*dim], 
        Gallery, 
        length*(i+1)/num-length*i/num, len(qmat), dim, threshold,length*i/num,
        GPUs[i%3])
        )
        )

    pool.close()
    pool.join()
    tuples=[]
    output_file = 'output_file_'+str(threshold)+'.npy'
    for a in ans:
        ret=a.get()
        tuples.extend(ret)
    np.array(tuples)
    np.save(output_file, tuples)

    

def main(query):
    qmat=read(query)
    run(qmat, filter_threshold)


if __name__ == "__main__":
    main(sys.argv[1])
