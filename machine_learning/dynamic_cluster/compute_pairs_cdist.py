# -*- coding: utf-8 -*-
#from __future__ import print_function
import os,sys
import numpy as np
from ctypes import *
import multiprocessing
from sklearn.preprocessing import normalize
import datetime
import time


#topk=1
#maxappearance=4
#time_start=time.mktime(time.strptime('20160101000000',"%Y%m%d%H%M%S"))
#filter_threshold= 0.5
pairs=500000000
dim=384
GPUs=[0,1,2,3]
#KEEP_FIRST=False
calc= CDLL('./libthreshold.so')
calc.calcthreshold.argtypes = [POINTER(c_float),POINTER(c_float) ,POINTER(c_int),c_float,POINTER(c_int) ,POINTER(c_int) ,POINTER(c_float) ]


def read_npy(f):
    t1 = datetime.datetime.now()
    #mat = np.loadtxt(f,dtype=np.float32, usecols=range(1,385))
    mat = np.load(f)
    t2 = datetime.datetime.now()
    print ('end load fealst', t2-t1)
    return normalize(mat)

#def get_id_time(fid):
#    id, tim = '', ''
#    key = fid.split('/')[-1].rstrip('.jpg')
#    ary = key.split('_')
#    if len(ary) == 6:
       # id = ary[0] + ary[1]
#        tim = ary[2]
#    else:
#        ary = key.split('-')
       # id = ary[0] + ary[1]
#        tmp = ary[2].split('_')
#        tim = '20' + tmp[0] + tmp[1]
#    tim=time.mktime(time.strptime(tim, "%Y%m%d%H%M%S"))-time_start
#    return tim


def read(f):
    t1 = datetime.datetime.now()
    mat = np.array(np.loadtxt(f, usecols=range(1,385)), 'f')
    time_list=map(get_id_time, os.popen("awk '{print$1}' "+f).read().splitlines())
    t2 = datetime.datetime.now()
    print ('end read file_features: ', t2-t1)
    return normalize(mat),np.array(time_list)

# def scoremapping(score):
#     return np.maximum(np.minimum(1.4084507*(1+score)/2-0.17746479,0.9999),0)
#
#
#
# def unmap(score):
#     return (score+0.17746479)*2/1.4084507-1

def do(i,query_l,query_r,lq,lg,dim,threshold,shift,gpu):
    global Query
    global Gallery
    print('batch ',i)
    for j in range(10000):
        print (i,'----->',j)
def do3(i,lq,lg,dim,threshold,shift,gpu):
    print('batch ',i)
    for j in range(10000):
        print (i,'----->',j)
def do2(i,query_l,query_r,time_l,time_r,lq,lg,dim,threshold,shift,gpu):
#    global time_list
    global Query
    query=Query[query_l:query_r]
    gallery=Query[:]
    time_batch=time_list[time_l:time_r]
    print ('start compute batch:', i)
    k=10**8
    index1=np.zeros(k,dtype="int32")
    index2=np.zeros(k,dtype="int32")
    scores=np.zeros(k,dtype="float32")
    time_dist=np.zeros(k,dtype="int32")
    
    cnt=0
    paras=np.array([lq,lg,dim,shift,cnt,k,gpu],dtype="int32")
    calc.calcthreshold(
    query.ctypes.data_as(POINTER(c_float)),
    gallery.ctypes.data_as(POINTER(c_float)),
    paras.ctypes.data_as(POINTER(c_int)),float(threshold),
    index1.ctypes.data_as(POINTER(c_int)),
    index2.ctypes.data_as(POINTER(c_int)),
    scores.ctypes.data_as(POINTER(c_float)),
#    time_dist.ctypes.data_as(POINTER(c_int)))
    assert(paras[4]<=k)
   
    # return zip(index1[:paras[4]],index2[:paras[4]],scoremapping(scores[:paras[4]]))
    return zip(index1[:paras[4]], index2[:paras[4]], scores[:paras[4]])


def get_cdist(qmat,threshold):
    global Query
 #   global time_list
 #   global Gallery
    t1 = datetime.datetime.now()
    Query=qmat.reshape(-1)
    #Gallery=Query
       
    length=len(qmat)
    print ('qmat length', length) 
#    assert(len(qmat)<400000)
    num=length/(pairs/length)
    print ('hoe many batchs:',num)
    # threshold=unmap(threshold)
    ans=[]   
    pool=multiprocessing.Pool(processes=6)
   
    for i in range(num):
        print ('batch:',i)
        print ('need GPU', i%6)
        t1 = datetime.datetime.now()
      #  print ('q[],lq,lg,dim,th,shift:', length*i/num*dim, length*(i+1)/num*dim, length*(i+1)/num-length*i/num, length, dim, threshold,length*i/num)
      #  ans.append(pool.apply_async(do,(i,Query[length*i/num*dim:length*(i+1)/num*dim],Gallery[:],length*(i+1)/num-length*i/num, length, dim, threshold,length*i/num,GPUs[i%len(GPUs)],))) 
        ans.append(pool.apply_async(do2,(i,length*i/num*dim,length*(i+1)/num*dim,length*i/num,length*(i+1)/num,length*(i+1)/num-length*i/num, length, dim, threshold,length*i/num,GPUs[i%len(GPUs)],)))
        t2 = datetime.datetime.now()
        print ('time:',t2-t1)
    t11=datetime.datetime.now()
    print ('end for load',t11-t1)
    pool.close()
    pool.join()
    t111=datetime.datetime.now()
    print ('end compute cdist:',t111-t1)
    tuples=[]
    output_file = 'cdist_'+str(threshold)
    for a in ans:
        ret=a.get()
        tuples.extend(ret)
    np.array(tuples)
    print ('pairs:', len(tuples))
    t2 = datetime.datetime.now()
    print ('end compute dist',t2-t1)
    return tuples
#    np.save(output_file, tuples)
#    t3 = datetime.datetime.now()
#    print ('end write' , t3-t2)
#    print ('out_put: ', output_file)
    

#def get_dist(query):
 #   global time_list
   # qmat,time_list=read(query)
   # print (time)
   # run(qmat,time_list, filter_threshold)


#if __name__ == "__main__":
#    main(sys.argv[1])
