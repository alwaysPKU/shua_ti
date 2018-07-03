# -*- coding: utf-8 -*-
import os,sys
import numpy as np
from ctypes import *
import multiprocessing
from sklearn.preprocessing import normalize
import datetime
import time
import compute_pairs_cdist as compute_dist
import cluster
import copy
import argparse
"""
动态聚类:
1. 选定需要动态聚类的次数n
2. 选定每次聚类的阈值threshold_n
先按照阈值从紧到松进行聚类,从每次聚类的簇挑出align*detect分值最大的图片作为代表,进行下次聚类的基础,直到结束.
"""

def get_time():
    return datetime.datetime.now()
					
def get_id_time(fid):
    # 通过fid,以2016.1.1为起点制作时间戳
    tim = ''
    key = fid.split('/')[-1].rstrip('.jpg')
    ary = key.split('_')
    if len(ary) == 6:
        # id = ary[0] + ary[1]
        tim = ary[2]
    else:
        ary = key.split('-')
        # id = ary[0] + ary[1]
        tmp = ary[2].split('_')
        tim = '20' + tmp[0] + tmp[1]
    tim=time.mktime(time.strptime(tim, "%Y%m%d%H%M%S"))-time_start
    return tim

def float_x(s):
    if s:
        return float(s)
    else:
        return 0


def read_test(f1,f2):
    """读文件1.读features文件得到features和相对时间戳,2.读参数文件得到打分"""
    #1.
    #features
    t1=get_time()
    print 'start read features and fid'
    mat_features=[]
    fid_list=[]
    mat_features=normalize(np.load(f1))
    #mat_features = normalize(np.loadtxt(f1,dtype='float32', usecols=range(1,385)))
    #时间戳
    #time_list=map(get_id_time, os.popen("awk '{print$1}' "+f1).read().splitlines())
    #fid
    #fid_list=os.popen("awk '{print$1}' "+f1).read().splitlines()
    #2.
    #打分
    file_fid='../test_data/403_fid'
    fid_list=os.popen('cat '+file_fid).read().splitlines()
    t2=get_time()
    print 'end read features, use %s s. start read scores'%(t2-t1)
    score_list=np.load(f2)
    #return time_list,mat_features, score_list, fid_list
    t3=get_time()
    print 'end read scores, use %s s'%(t3-t2)
    return fid_list,mat_features,score_list

def read_new(f1,f2):
    """读文件1.读features文件得到features和相对时间戳,2.读参数文件得到打分"""
    #1.
    #features
    t1=get_time()
    print 'start read features and fid'
    mat_features=[]
    fid_list=[]
    with open(f1) as f:
        for line in f.readlines():
            ary=line.strip().split(' ')
            fid_list.append(ary[0])
            mat_features.append(map(float,ary[1:]))
    mat_features=normalize(np.array(mat_features,dtype='float32'))
    #mat_features = normalize(np.loadtxt(f1,dtype='float32', usecols=range(1,385)))
    #时间戳
    #time_list=map(get_id_time, os.popen("awk '{print$1}' "+f1).read().splitlines())
    #fid
    #fid_list=os.popen("awk '{print$1}' "+f1).read().splitlines()
    #2.
    #打分
    t2=get_time()
    print 'end read features, use %s s. start read scores'%(t2-t1)
    score_list = [float_x(one_line.strip().split(',')[-3])*float_x(one_line.strip().split(',')[-2]) \
        for one_line in open(f2).readlines()]
    #return time_list,mat_features, score_list, fid_list
    t3=get_time()
    print 'end read scores, use %s s'%(t3-t2)
    return fid_list,mat_features,np.array(score_list)

def read(f1,f2):
    """读文件1.读features文件得到features和相对时间戳,2.读参数文件得到打分"""
    #1.
    #features
    t1=get_time()
    print 'start read features and fid'
    mat_features = normalize(np.array(np.loadtxt(f1, usecols=range(1,385)), 'f'))
    #时间戳
    #time_list=map(get_id_time, os.popen("awk '{print$1}' "+f1).read().splitlines())
    #fid
    fid_list=os.popen("awk '{print$1}' "+f1).read().splitlines()
    #2.
    #打分
    t2=get_time()
    print 'end read features, use %s s. start read scores'%(t2-t1)
    score_list = [float_x(one_line.strip().split(',')[-3])*float_x(one_line.strip().split(',')[-2]) \
        for one_line in open(f2).readlines()]
    #return time_list,mat_features, score_list, fid_list
    t3=get_time()
    print 'end read scores, use %s s'%(t3-t2)
    return fid_list,mat_features,np.array(score_list)

def loop_cluster(index_rp,labels,mat_features,score_list,threshold,i):
    # 建标签索引 
    t1=get_time()
    print 'pre for the %d cluster'%(i+1)    
    labels_index={}
    index_rp_res=[]
    rp_index={}
    if i==1:
        for j,label in enumerate(labels):
            if not label in labels_index:
                labels_index[label]=[]
            labels_index[label].append(j)
    else:
        for index,label in zip(index_rp,labels):
            if not label in labels_index:
                labels_index[label]=[]
            labels_index[label].append(index)
    #print 'labels--->',len(labels_index)
    #count=0
    #for ic in labels_index.values():
    #    count+=len(ic)
    #print 'labels.values-->',count
    print 'the %d cluster has %d clusters'%(i,len(labels_index))    
    for index_lst in labels_index.values():
        #labels_first_lst.append(label)
        tmp=0
        mark=0
        for index in index_lst:
            if score_list[index]>=tmp:
                tmp=score_list[index]
                mark = index
        index_rp_res.append(mark)
        rp_index[mark]=index_lst
    #print '===='
    #print 'rp_index--->',len(rp_index)
    #count=0
    #for ic in rp_index.values():
    #    count+=len(ic)
    #print '--->',count
    #print '===='
    t2=get_time()
    print 'end pre,use %s s.  start the No.%d cluster by threshold=%f:'%(t2-t1,i+1,threshold)
    print '------------------------------------'
    #print '==========',len(index_rp_res),mat_features.shape
    new_features=mat_features[index_rp_res]
    pairs_cdists=compute_dist.get_cdist_multi(new_features,threshold,gpus)
    labels_2=cluster.cluster(pairs_cdists, len(labels_index))
    t3=get_time()
    print 'end %d cluster, use %s s'%(i+1, t3-t2)
    #print '---->',len(rp_index)
    #count=0
    #for ic in rp_index.values():
    #    count+=len(ic)
    #print '----->',count
    return index_rp_res, labels_2, rp_index

def main(f1,f2,threshold,out_file):#,f2
    #time_list,mat_features,score_list,fid_list=read(f1,f2)
    fid_list, mat_features,score_list=read_test(f1,f2)
    num=len(fid_list)

    t1=get_time()
    print 'start the No.1 cluster by threshold=%f:'%threshold[0]
    print '------------------------------------'
    #按照时间戳排序:
    #for timestap,feature,score,fid in sorted(zip(time_list,mat_features,score_list,fid_list),key=lambda x:x[0]):
    # 计算pairs_dist:格式[[index1,index2,cdist],]
    pairs_cdists=compute_dist.get_cdist_multi(mat_features,threshold[0],gpus)
    # 第一次聚类:
    labels=cluster.cluster(pairs_cdists,num)
    #print '=====len(labels)',len(labels),labels[:30]
    # loop cluster
    t2=get_time()
    print 'end 1 cluster, use %s s'%(t2-t1)
    print 'start loop cluster:'
    index_rps_list=[] #2维  存放每次参与聚类的index
    labels_rps_list=[] #2维 存放每次参与聚类的index 对应的labels
    rp_index_list=[] #2维但长度-1  存放 rp_index-->index_list词典
    index_rps_list.append(range(num))
    labels_rps_list.append(labels)
    for i,thr in enumerate(threshold):
        if i==0:
            continue
        idex_rp,labels_i,rp_index=loop_cluster(index_rps_list[i-1],labels_rps_list[i-1],mat_features,score_list,thr,i)
        index_rps_list.append(idex_rp)
        labels_rps_list.append(labels_i)
        rp_index_list.append(rp_index)
    
    # merge clusters
    t3=get_time()
    #print '===================='
    #print 'index'
    #for i in index_rps_list:
    #    print len(i)
    #print 'labels'
    #for i in labels_rps_list:
    #    print len(i)
    #print 'rp'
    #for i in rp_index_list:
    #    print len(i)
    #    count =0
    #    for c in i.values():
    #        count +=len(c)
    #    print count
    #print '===================='
    print 'end loop cluster, use %s s'%(t3-t2)
    print 'num of final clusters:',len(set(labels_rps_list[-1]))
    print 'start merge labels and write'
    step=len(rp_index_list)
    labels_rp_result={}
    for rp, label in zip(index_rps_list[step],labels_rps_list[step]):
        if not label in labels_rp_result:
            labels_rp_result[label]=[]
        labels_rp_result[label].append(rp)
    
    #print '========================'
    #print len(labels_rp_result)
    #count=0
    #for i in labels_rp_result.values():
    #    count+=len(i)
    #print count
    #print '========================'
    #print 'end 1---------->',get_time()-t3
    for i in range(step-1,-1,-1):
        #print 'stt------->',i
        for k,v in labels_rp_result.items():
            #print '    ------->',k,v
            s=copy.deepcopy(v)
            for index in s:
                labels_rp_result[k].extend(rp_index_list[i][index])
            labels_rp_result[k]=list(set(labels_rp_result[k]))
            
        #print '========================',i
        #print len(labels_rp_result)
        #count=0
        #for i in labels_rp_result.values():
        #    count+=len(i)
        #print count
        #print '========================'
    t4 = get_time()
    print 'end merge labels, use %s s'%(t4-t3)
    #return labels_rp_result
    #结果输出
    f=open(out_file,'w')
    labels_full=[]
    index_full=[]
    for k,v in labels_rp_result.items():
        for index in v:
            labels_full.append(k)
            index_full.append(index)
    for fid, label in sorted(zip(index_full,labels_full),key=lambda x:x[0]):
        f.write(fid_list[fid]+' '+str(label)+'\n')
    f.close()
    t5=get_time()
    print 'end write result, use %s s'%(t5-t4)

def parse_args():
    parser=argparse.ArgumentParser(description="this is dynamic cluster")
    parser.add_argument("-f","--feature",help="the features file path")
    parser.add_argument("-p","--param",help="the parameter file path")
    parser.add_argument("-t","--thresholds",default='0.9,0.8,0.7',dest="thresholds",help="the threshold list, split with ',',default=0.9,0.8,0.7 ")
    parser.add_argument("-o","--output",default='res_default',help="the output file")
    parser.add_argument("-g","--gpus",default='0,1,2,3,4,5',help="the gpu index,split with ',',default0,1,2,3,4,5")
    args=parser.parse_args()
    return args

if __name__ == "__main__":
    print get_time()
    args=parse_args()
    feature_file=args.feature
    params_file=args.param
    thresholds=map(float,args.thresholds.split(','))
    for i in thresholds:
        if i >=1 or i<=0.4:
            print 'illegal thresholds'
            exit()
    thresholds.sort()
    thresholds.reverse()
    out_put=args.output
    gpus=map(int,args.gpus.split(','))
    #feature_file=sys.argv[1]
    #thresholds=[0.9,0.8,0.7]
    #params_file=sys.argv[2]
    #out_put=sys.argv[3]
    # 以2016.1.1为起点
    print args
    print '-in_put: %s\n-feature: %s\n-params: %s\n-thresholds: %s\n-gpus: %s\n-out_put: %s\n'%(sys.argv[0],\
        args.feature,args.param,args.thresholds,args.gpus,args.output)
    time_start=time.mktime(time.strptime('20160101000000',"%Y%m%d%H%M%S"))
    main(feature_file,params_file,thresholds,out_put)
    print get_time()


