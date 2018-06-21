# -*- coding: utf-8 -*-
import os,sys
import numpy as np
from ctypes import *
import multiprocessing
from sklearn.preprocessing import normalize
import datetime
import time
import compute_pairs_cdist as compute_dist


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
    time_list=map(get_id_time, os.popen("awk '{print$1}' "+f1).read().splitlines())
    #fid
    fid_list=os.popen("awk '{print$1}' "+f1).read().splitlines()
    #2.
    #打分
    score_list = [float(one_line.strip().split(',')[-3])*float(one_line.strip().split(',')[-2]) \
        for one_line in open(f2).readlines()]
    return time_list,mat_features, score_list, fid_list
    

def main(f1,f2):
    time_list,mat_features,score_list,fid_list=read(f1,f2)
    cnt=0
    for timestap,feature,score,fid in sorted(zip(time_list,mat_features,score_list,fid_list),key=lambda x:x[0]):
        print timestap,score,fid
        cnt+=1
        if cnt > 1000:
            break

if __name__ == "__main__":
    feature_file=sys.argv[1]
    params_file=sys.argv[2]
    # 以2016.1.1为起点
    time_start=time.mktime(time.strptime('20160101000000',"%Y%m%d%H%M%S"))
    main(feature_file,params_file)


