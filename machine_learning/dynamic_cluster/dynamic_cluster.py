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


def read(f1,f2):
    """读文件1.读features文件得到features和相对时间戳,2.读参数文件得到打分"""
    #1.
    #features
    mat_features = normalize(np.array(np.loadtxt(f1, usecols=range(1,385)), 'f'))
    #时间戳
    #time_list=map(get_id_time, os.popen("awk '{print$1}' "+f1).read().splitlines())
    #fid
    fid_list=os.popen("awk '{print$1}' "+f1).read().splitlines()
    #2.
    #打分
    score_list = [float(one_line.strip().split(',')[-3])*float(one_line.strip().split(',')[-2]) \
        for one_line in open(f2).readlines()]
    #return time_list,mat_features, score_list, fid_list
    return fid_list,mat_features,np.array(score_list)

def loop_cluster(index_rp,labels,mat_features,score_list,threshold,i):
    # 建标签索引 
    labels_index={}
    index_rp=[]
    rp_index={}
    if i==0:
        for i,label in enumerate(labels):
            if not label in labels_index.keys():
                labels_index[label]=[]
            labels_index[label].append(i)
    else:
        for index,label in zip(index_rp,labels):
            if not label in labels_index.keys():
                labels_index[label]=[]
            labels_index[label].append(index)
        
    for index_lst in labels_index.values():
        #labels_first_lst.append(label)
        tmp=0
        mark=0
        for index in index_lst:
            if score_list[index]>tmp:
                tmp=score_list[index]
                mark = index
        index_rp.append(mark)
        rp_index[mark]=index_lst
        mark=0
    # num2=len(idex_rp)
    new_features=mat_features[index_rp]
    pairs_cdists=compute_dist.get_cdist(new_features,threshold)
    labels_2=cluster.cluster(pairs_cdists, len(labels_index))
    return index_rp, labels_2, rp_index

def main(f1,f2,threshold,out_file):#,f2
    #time_list,mat_features,score_list,fid_list=read(f1,f2)
    fid_list, mat_features,score_list=read(f1,f2)
    num=len(fid_list)
    #按照时间戳排序:
    #for timestap,feature,score,fid in sorted(zip(time_list,mat_features,score_list,fid_list),key=lambda x:x[0]):
    # 计算pairs_dist:格式[[index1,index2,cdist],]
    pairs_cdists=compute_dist.get_cdist(mat_features,threshold[0])
    # 第一次聚类:
    labels=cluster.cluster(pairs_cdists,num)
    # loop cluster
    index_rps_list=[] #2维
    labels_rps_list=[] #2维
    rp_index_list=[] #2维但长度-1
    index_rps_list.append(range(num))
    labels_rps_list.append(labels)
    for i,thr in enumerate(threshold):
        if i==0:
            continue
        idex_rp,labels_i,rp_index=loop_cluster(index_rps_list[i],labels[i],mat_features,score_list,thr,i)
        index_rps_list.append(idex_rp)
        labels_rps_list.append(labels_i)
        rp_index_list.append(rp_index)
    # merge clusters
    step=len(rp_index_list)
    labels_rp_result={}
    for rp, label in zip(index_rps_list[step],labels_rps_list[step]):
        if not label in labels_rp_result.keys():
            labels_rp_result[label]=[]
        labels_rp_result[label].append(rp)
    for i in range(step-1,-1,-1):
        for k,v in labels_rp_result.items():
            for index in v:
                labels_rp_result[k].extend(rp_index_list[i][index])
            labels_rp_result[k]=set(labels_rp_result[k])
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

if __name__ == "__main__":
    feature_file=sys.argv[1]
    thresholds=[0.7,0.6,0.5]
    params_file=sys.argv[2]
    out_put=sys.argv[3]
    # 以2016.1.1为起点
    time_start=time.mktime(time.strptime('20160101000000',"%Y%m%d%H%M%S"))
    main(feature_file,params_file,thresholds,out_put)


