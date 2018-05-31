import os,shutil,sys
import time as time
import numpy as np
from scipy.spatial.distance import pdist
import string
from scipy.cluster.hierarchy import *
import datetime
import random
import ImageFont,Image,ImageDraw
from pyflann import *
from sklearn.preprocessing import normalize

def thumb(imglist,variance,output):
    picsize=150
    cur_width = 0
    cur_height= 20
    nth=0
    size=min(len(imglist),50)
    width = 1500
    nEachRow=width/picsize
    height = 20+min(picsize+(size-1)/nEachRow*picsize,750)
    row_num=(height-20)/picsize
    merge_img = Image.new('RGB', (width,height), 0xffffff)
    for img in imglist:
        nth += 1
        fp = open('result/shoptest/'+img,'r')
        img = Image.open(fp)
        if img.mode != 'RGB':
            img = img.convert('RGB')
        merge_img.paste(img.resize((picsize,picsize),Image.BICUBIC), (cur_width, cur_height))
        cur_width += picsize
        if nth%nEachRow==0:
            cur_height+=picsize
            cur_width=0
        if nth==nEachRow*row_num:
            break
    dl= ImageDraw.Draw(merge_img)
    font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf', 20)
    msg1="Variance = "+str(round(variance,3))
    dl.text((0,0),msg1, fill="red",font=font)
    merge_img.save(output,quality=100)
    

def pastePart(merge_img,imglist,kind):
    cur_width=620-kind*160
    cur_height=60
    nEachLine=3
    picsize=200
    nth=0
    for pic in imglist[:9]:
        nth += 1
        fp = open('result/shoptest/'+pic,'r')
        img = Image.open(fp).resize((picsize,picsize),Image.BICUBIC)
        if img.mode != 'RGB':
            img = img.convert('RGB')
        if nth%nEachLine==1:
            cur_height=60
            cur_width-=200*(1-2*kind)
        merge_img.paste(img, (cur_width, cur_height))
        fp.close()
        cur_height += picsize
    return merge_img

    

def merge(lid, rid,dist,output_file):  
    width=1280
    height=720
    merge_img = Image.new('RGB', (width,height), 0xffffff)
    merge_img=pastePart(merge_img,lid,0)
    merge_img=pastePart(merge_img,rid,1)        

    dl= ImageDraw.Draw(merge_img)
    dl.line([width/2,0,width/2,height],fill = 'red')
    dl.line([(20,60),(20,660),(620,660),(620,60),(20,60)],'green')
    dl.line([(660,60),(660,660),(1260,660),(1260,60),(660,60)],'green')

    font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf', 20)
    msg1="Dist = "+str(round(dist,3))
    dl.text((0,0),msg1, fill="red",font=font)

    merge_img.save(output_file, quality=100)
    



def read(path):
    cnt=0
    fin=open(path)
    print "started",datetime.datetime.now()
    names=[]
    images={}
    labels=[]
    features=[]
    i=0
    line=fin.readline()
    last=""
    while line:
        array=line[:-1].split(" ")
        line=fin.readline()
        imgname=array[0]
        this=array[1]
#        if last!=this and last!="" and len(images[last])<20: 
#            images.pop(last)
            
        if not images.has_key(this):
            images[this]=[]
        elif len(images[this])>20:
            continue
        names.append(imgname)
        labels.append(this)
        features.append(map(float,array[2:]))
        images[this].append(i)
        i+=1
        last=this
        if i%10000==0:
            print i
        if i>200000:
            break
    return np.array(names),images,np.array(labels),normalize(np.array(features,dtype="f"))


def get_worst_clusters(features,images):
    variances=[]
    for value in images.values():
        variances.append(np.sum(np.var(features[value,],axis=0)))
#        variances=np.sum(np.var(features[images.values(),],axis=1),axis=1)
    variances=np.array(variances)
    print variances.shape
    indexs=np.argpartition(-variances,100)[:100]
    return np.array(images.keys())[indexs],variances[indexs]


def getANN(features,labels,images):
    flann = FLANN()
    K=100
    results,dists=flann.nn(features,features,K,algorithm="kdtree")
    ind=np.tile(np.arange(results.shape[0]).reshape(-1,1),results.shape[1])
    other= labels[results]!=labels[ind]
    close= dists<0.7
    wh=np.where( other &  close )
    print len(wh[0])
    ret=[labels[wh[0]],labels[results[wh]]]
    #print other,close,other&close
    D=list(dists[wh])
    return ret+[D]

def time():
    return datetime.datetime.now()
        
        
def main( feature_file,tagdest,kind): 
    names,images,labels,features=read(feature_file)
    print "read!",time()
    if kind&1:
        worstClusters,V=get_worst_clusters(features,images)
        print "worst clusters done!",time()
        cnt=0
        for cluster in worstClusters[:100]:
            thumb(names[images[cluster]],V[cnt],os.path.join(tagdest,"1_"+str(cnt)+".jpg"))
            cnt+=1
        print "finish drawing",time()
    if kind&2:
        cnt=0
        results=getANN(features,labels,images)
        print "ANN done!",time()
        lasta=""
        lastb=""
        for a,b,dist in sorted(zip(*results)): 
            if a==lasta and b==lastb:
                continue
            merge(names[images[a]],names[images[b]],dist,os.path.join(tagdest,"2_"+str(cnt)+".jpg"))
            cnt+=1
            lasta=a
            lastb=b
            if cnt>100:
                break


if __name__ == "__main__":
    feature_file=sys.argv[1]
    tagdest=sys.argv[2]
    if not os.path.exists(tagdest):
        os.makedirs(tagdest)
    if len(sys.argv)>3:
        kind=int(sys.argv[3])
    else:
        kind=3
    main(feature_file,tagdest,kind)
