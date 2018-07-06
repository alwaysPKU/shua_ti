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
    '''
    通过fid解析出时间戳(相对于20160101的时间戳,到秒)
    :param fid: fid
    :return: 时间戳int
    '''
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
    '''
    把字符串参数转化为float,因为有的是空字符串,所以要判定
    :param s: 参数字符串(可能是align / detect分数等等)
    :return: float(s)
    '''
    if s:
        return float(s)
    else:
        return 0


def read_test(f1,f2):
    '''
    方便调试的读文件
    :param f1: features的二进制文件
    :param f2: score的二进制文件
    :return: 1.fid列表 2.features矩阵 3.分数列表.  按index一一对应
    '''
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
    return fid_list,mat_features,np.array(score_list)

def read_new(f1,f2):
    '''
    正常的读文件
    :param f1: features 字符串文件
    :param f2: 参数文件
    :return:1.fid列表 2.features矩阵 3.分数列表.  按index一一对应
    '''
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
    '''
    老的读文件,有点慢,废弃.loadtxt很慢
    :param f1: 
    :param f2: 
    :return: 
    '''
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
    '''
     第i次聚类,i>=2
    :param index_rp: 第i-1次聚类的index
    :param labels: 地i-1次聚类的labels
    :param mat_features: 全量的features矩阵
    :param score_list: 全量的score
    :param threshold: 第i次聚类的阈值
    :param i: 第i次聚类的下标符号
    :return: 1.第i次聚类的代表;2.第i次聚类的labels;3代表对应的被代表index组成的dict,用来最后的merge
    '''
    # 建标签索引 
    t1=get_time()
    print 'pre for the %d cluster'%(i+1)    
    labels_index={} # key是label,value是该label对应的index组成的list
    index_rp_res=[] # 下一轮作为代表参与聚类的index
    rp_index={}     # key是代表,value是被代表的list,包括其本身.
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
    labels_2=cluster.cluster(pairs_cdists, len(labels_index)) #代表们的聚类结果
    t3=get_time()
    print 'end %d cluster, use %s s'%(i+1, t3-t2)
    #print '---->',len(rp_index)
    #count=0
    #for ic in rp_index.values():
    #    count+=len(ic)
    #print '----->',count
    return index_rp_res, labels_2, rp_index

def loop_cluster_weighted_feature(index_rp,labels,rp_index,mat_features,score_list,threshold,i):
    '''
     第i次聚类,i>=2
    :param index_rp: 第i-1次聚类的index
    :param labels: 地i-1次聚类的labels
    :param mat_features: 全量的features矩阵
    :param score_list: 全量的score
    :param threshold: 第i次聚类的阈值
    :param i: 第i次聚类的下标符号
    :return: 1.第i次聚类的代表;2.第i次聚类的labels;3代表对应的被代表index组成的dict,用来最后的merge
    '''
    # 建标签索引 
    t1=get_time()
    print 'pre for the %d cluster'%(i+1)    
    labels_index={} # key是label,value是该label对应的index组成的list
    index_rp_res=[] # 下一轮作为代表参与聚类的index
    rp_index_tmp={}     # key是代表,value是被代表的list,包括其本身.
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
        rp_index_tmp[index_lst[0]]=index_lst
        index_rp_res.append(index_lst[0])
    if not len(rp_index) == 0:
        for k,v_list in rp_index_tmp.items():
            for v in copy.deepcopy(v_list):
                rp_index_tmp[k].extend(rp_index[v])
            rp_index_tmp[k]=list(set(rp_index_tmp[k]))
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
    for j in xrange(len(new_features)):
        if args.weighting_mode==1:#分数直接加权
            scores_j=score_list[rp_index_tmp[index_rp_res[j]]]
        elif args.weighting_mode==2:#平方加权
            scores_j=score_list[rp_index_tmp[index_rp_res[j]]]
            scores_j=scores_j*scores_j   
        features_j=mat_features[rp_index_tmp[index_rp_res[j]]]
        new_features[j]=normalize(np.sum(scores_j.reshape((-1,1))*features_j,axis=0).reshape((1,-1)))
    
    pairs_cdists=compute_dist.get_cdist_multi(new_features,threshold,gpus)
    labels_2=cluster.cluster(pairs_cdists, len(labels_index)) #代表们的聚类结果
    t3=get_time()
    print 'end %d cluster, use %s s'%(i+1, t3-t2)
    #print '---->',len(rp_index)
    #count=0
    #for ic in rp_index.values():
    #    count+=len(ic)
    #print '----->',count
    return index_rp_res, labels_2, rp_index_tmp

def main(f1,f2,threshold,out_file):#,f2
    '''
    主程序
    :param f1:features文件 
    :param f2: 参数文件
    :param threshold: 阈值列表,list
    :param out_file: 输出文件
    :return: None
    '''
    #time_list,mat_features,score_list,fid_list=read(f1,f2)
    if args.read_mode==0:
        fid_list, mat_features,score_list=read_test(f1,f2)
    elif args.read_mode==1:        
        fid_list, mat_features,score_list=read_new(f1,f2)
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
    merge_write(fid_list,rp_index_list,index_rps_list,labels_rps_list,out_file)

def main_weighted(f1,f2,threshold,out_file):
    '''
    主程序,但是不同的挑选代表方式
    :param f1:features文件 
    :param f2: 参数文件
    :param threshold: 阈值列表,list
    :param out_file: 输出文件
    :return: None
    '''
    #time_list,mat_features,score_list,fid_list=read(f1,f2)
    if args.read_mode=='t':
        fid_list, mat_features,score_list=read_test(f1,f2)
    elif args.read_mode=='n':        
        fid_list, mat_features,score_list=read_new(f1,f2)
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
    #rp_index_list=[] #2维但长度-1  存放 rp_index-->index_list词典
    rp_index={} # 对比差别!!!!!在更新,不是list了
    index_rps_list.append(range(num))
    labels_rps_list.append(labels)
    for i,thr in enumerate(threshold):
        if i==0:
            continue
        idex_rp,labels_i,rp_index=loop_cluster_weighted_feature(index_rps_list[i-1],labels_rps_list[i-1],rp_index,mat_features,score_list,thr,i)
        index_rps_list.append(idex_rp)
        labels_rps_list.append(labels_i)
        #rp_index_list.append(rp_index)
    
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
    merge_write_weighted(fid_list,rp_index,index_rps_list,labels_rps_list,out_file)
    

def merge_write_weighted(fid_list,rp_index_list,index_rps_list,labels_rps_list,out_file):
    t1=get_time()
    print 'start merge labels and write'
    #step=len(rp_index_list)
    labels_rp_result={}
    for rp, label in zip(index_rps_list[-1],labels_rps_list[-1]):
        if not label in labels_rp_result:
            labels_rp_result[label]=[]
        labels_rp_result[label].extend(rp_index_list[rp])
    
    
    #print '========================'
    #print len(labels_rp_result)
    #count=0
    #for i in labels_rp_result.values():
    #    count+=len(i)
    #print count
    #print '========================'
    #print 'end 1---------->',get_time()-t3
    #for i in range(step-1,-1,-1):
        #print 'stt------->',i
    #    for k,v in labels_rp_result.items():
            #print '    ------->',k,v
    #        s=copy.deepcopy(v)
    #        for index in s:
    #            labels_rp_result[k].extend(rp_index_list[i][index])
    #        labels_rp_result[k]=list(set(labels_rp_result[k]))
            
        #print '========================',i
        #print len(labels_rp_result)
        #count=0
        #for i in labels_rp_result.values():
        #    count+=len(i)
        #print count
        #print '========================'
    t4 = get_time()
    print 'end merge labels, use %s s'%(t4-t1)
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

def merge_write(fid_list,rp_index_list,index_rps_list,labels_rps_list,out_file):
    t1=get_time()
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
    print 'end merge labels, use %s s'%(t4-t1)
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
    '''
     参数解析
    :return: fature,params,threshold,gpu,output
    '''
    parser=argparse.ArgumentParser(description="this is dynamic cluster. 动态聚类:给定阈值list动态聚类,可选择不同的mode")
    parser.add_argument("-f","--feature",help="the features file path")
    parser.add_argument("-p","--param",help="the parameter file path")
    parser.add_argument("-t","--thresholds",default='0.8,0.7',dest="thresholds",\
                        help="the threshold list, split with ',' ,\n default=0.8,0.7 ")
    parser.add_argument("-o","--output",default='default',help="the output file")
    parser.add_argument("-g","--gpus",default='0,1,2,3,4,5',help="the gpu index,split with ',' ,\
                        default=0,1,2,3,4,5")
    parser.add_argument("-r","--read_mode",default='t',choices=['t','n'],help="the read mode.\
                        default is t, t is test, n is normal read")
    parser.add_argument("-m","--choice_mode",default='sample',choices=['sample','weighting'],\
                        help="how to chice the cluster' reference, the default is sample.\
                        sample:choice the biggest score(align*detect) as the cluster's sample.\
                        weighting: a_i=score_i f=Σa_i*f_i/Σa_i.")
    parser.add_argument("-w","--weighting_mode",type=int,default=1,choices=[1,2],help="when the \
                        choice_mode is weighting, the weighting_mode=1 means f=Σa_i*f_i/Σa_i.\
                        the weighting_mode=2 means Σa_i²*f_i/Σa_i².")
    args=parser.parse_args()
    return args

if __name__ == "__main__":
    t1=get_time()
    print '######################################################'
    print '#############  start dynamic cluster  ################'
    print '######################################################'
    print t1,'\n'
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
    if args.output=='default':
        if args.choice_mode=='weighting':
            out_put='labels_'+args.thresholds+'_'+str(args.choice_mode)+'_'+str(args.weighting_mode)
        elif args.choice_mode=='sample':
            out_put='labels_'+args.thresholds+'_'+str(args.choice_mode)
    else:
        out_put=args.output
    gpus=map(int,args.gpus.split(','))
    #feature_file=sys.argv[1]
    #thresholds=[0.9,0.8,0.7]
    #params_file=sys.argv[2]
    #out_put=sys.argv[3]
    # 以2016.1.1为起点
    print args
    print '-->in_put: %s\n-->read_mode: %s\n-->feature: %s\n-->params: %s\n-->choice_mode: %s\n\
-->weighting_mode :%s\n-->thresholds: %s\n-->gpus: %s\n-->out_put: %s\n'\
            %(sys.argv[0],args.read_mode,args.feature,args.param,args.choice_mode,\
            args.weighting_mode,args.thresholds,args.gpus,out_put)
    time_start=time.mktime(time.strptime('20160101000000',"%Y%m%d%H%M%S"))
    if args.choice_mode=='sample':
        main(feature_file,params_file,thresholds,out_put)
    elif args.choice_mode=='weighting':
        main_weighted(feature_file,params_file,thresholds,out_put)
    t2=get_time()
    print t2
    print 'the total time:',t2-t1,t2
    print '######################################################'
    print '###############  end dynamic cluster  ################'
    print '######################################################'
