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

def thumb(imglist,label,variance,output):
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
#    for img in imglist:
    length = len(imglist)
    step = length/50 + 1
    for index in xrange(0, len(imglist) ,step):
       # img = name_align_dict[img]
       # print img
        img = imglist[index]
        nth += 1
        if not os.path.exists("imgs/"+img):
            os.system("wget http://192.168.3.253:9333/"+img+" -P imgs/ >/dev/null 2>&1")
        fp = open("imgs/"+img,'r')
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
    msg1="Variance = "+str(round(variance,3))+'    label: '+label
    dl.text((0,0),msg1, fill="red",font=font)
    merge_img.save(output,quality=100)
    

def pastePart(merge_img,imglist,kind,params):
    cur_width=620-kind*160
    cur_height=60
    nEachLine=3
    picsize=200
    nth=0
    font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf', 15)
    for pic,param in zip(imglist[:9],params[:9]):
        nth += 1
        if not os.path.exists("imgs/"+pic):
            os.system("wget http://192.168.3.253:9333/"+pic+" -P imgs/ >/dev/null 2>&1")
        
        fp = open("imgs/"+pic,'r')
        img = Image.open(fp).resize((picsize,picsize),Image.BICUBIC)
        if img.mode != 'RGB':
            img = img.convert('RGB')
        if nth%nEachLine==1:
            cur_height=60
            cur_width-=200*(1-2*kind)
        merge_img.paste(img, (cur_width, cur_height))
        dl = ImageDraw.Draw(merge_img)
        mark=0
        for i in param:
             dl.text((cur_width, cur_height+mark),i.strip(),fill='red',font=font)
             mark += 15
        fp.close()
        cur_height += picsize
    return merge_img

    

def merge(llabel_a, rlabel_b,lid, rid,dist,output_file, l_p_id, r_p_id, l_params,r_params,l_daibiao,r_daibiao):  
    width=1280
   # height=720
    height=760
    merge_img = Image.new('RGB', (width,height), 0xffffff)
    merge_img=pastePart(merge_img,lid,0,l_params)
    merge_img=pastePart(merge_img,rid,1,r_params)        

    dl= ImageDraw.Draw(merge_img)
    dl.line([width/2,0,width/2,height],fill = 'red')
    dl.line([(20,60),(20,660),(620,660),(620,60),(20,60)],'green')
    dl.line([(660,60),(660,660),(1260,660),(1260,60),(660,60)],'green')

    font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf', 20)
    font2=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf', 10)
    consine_dist = (2-dist)/2.0
    msg1="Dist = "+str(round(dist,3))+'   Consine_dist:'+str(round(consine_dist,3))+'       l_label: '+llabel_a+'                   r_label: '+rlabel_b
    dl.text((0,0),msg1, fill="red",font=font)
    dl.text((20,49),l_daibiao,fill='red',font=font2)
    dl.text((660,49),r_daibiao,fill='red',font=font2)
    l_mark = 0
    r_mark = 0
    for i in l_p_id[:9]:
        if i == l_daibiao:
            dl.text((20,660+l_mark),i,fill='red',font=font2)
        else:
            dl.text((20,660+l_mark),i,fill='green',font=font2)
        l_mark+=10
    for i in r_p_id[:9]:
        if i == r_daibiao:
            dl.text((660,660+r_mark),i,fill='red',font=font2)
        else:
            dl.text((660,660+r_mark),i,fill='green',font=font2)
        r_mark += 10    
    merge_img.save(output_file, quality=100)
    



def read(path, path_label,path_align):
    name_label_dict={}
    name_align_dict={}
    name_param_dict={}
    with open(path_label) as r:
        line = r.readline().strip()
        while line:
            ary = line.split(' ')
            name_label_dict[ary[0]]=ary[1]
            line=r.readline().strip()
    with open(path_align) as r:
        line = r.readline().strip()
        while line:
            line_ary=line.split(',')
            if line_ary[0]!='source':
                name_align_dict[line_ary[2]]=str(line_ary[6]+','+line_ary[7]).lstrip('"').rstrip('"')
                name_param_dict[line_ary[2]]=line_ary[-7:]
            line = r.readline()


    cnt=0
    fin=open(path)
    print "started",datetime.datetime.now()
    names=[]
    p_id = []
    images={}
    labels=[]
    features=[]
    params=[]
    i=0
    line=fin.readline()
    last=""
    while line:
       # array=line[:-1].split(" ")
        array=line.strip().split(' ')
        line=fin.readline()
        imgname=name_align_dict[array[0]]
        parameter=name_param_dict[array[0]]
#        print imgname


       # this=array[1]
        this=name_label_dict[array[0]]
#        if last!=this and last!="" and len(images[last])<20: 
#            images.pop(last)
            
        if not images.has_key(this):
            images[this]=[]
  #2      elif len(images[this])>20:
  #2          continue
        p_id.append(array[0])
        params.append(parameter)
        names.append(imgname)
        labels.append(this)
       # features.append(map(float,array[2:]))
        features.append(map(float,array[1:]))
        images[this].append(i)
        i+=1
        last=this
        if i%10000==0:
            print i
        if i>500000:
            break
    return np.array(names),images,np.array(labels),normalize(np.array(features,dtype="f")),np.array(p_id),np.array(params)


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
    return ret+[D]+[wh[0]]+[results[wh]]

def time():
    return datetime.datetime.now()
        
        
def main( feature_file,labels_file,align_file,tagdest,kind): 
    names,images,labels,features,p_id,params=read(feature_file, labels_file, align_file)
    print "read!",time()

    if kind&1:
        worstClusters,V=get_worst_clusters(features,images)
        print "worst clusters done!",time()
        cnt=0
        for cluster in worstClusters[:100]:
           # thumb(names[images[cluster]],V[cnt],os.path.join(tagdest,"1_"+str(cnt)+".jpg"))
            thumb(names[images[cluster]],cluster,V[cnt],os.path.join(tagdest,"1_"+str(cnt)+".jpg"))
            cnt+=1
        print "finish drawing",time()
    if kind&2:
        cnt=0
        results=getANN(features,labels,images)
        print "ANN done!",time()
        lasta=""
        lastb=""
        for a,b,dist,l_index,r_index in sorted(zip(*results)): 
            if a==lasta and b==lastb:
                continue
            merge(a, b, names[images[a]],names[images[b]],dist,os.path.join(tagdest,"2_"+str(cnt)+".jpg"),p_id[images[a]], p_id[images[b]],params[images[a]],params[images[b]],p_id[l_index],p_id[r_index])
            cnt+=1
            lasta=a
            lastb=b
            if cnt>100:
                break

if __name__ == "__main__":
    feature_file=sys.argv[1] # xxx_featlst
    labels_file=sys.argv[2] # labels_xxx
    align_file=sys.argv[3] # xxx_paramerters
    tagdest=sys.argv[4]
    if not os.path.exists(tagdest):
        os.makedirs(tagdest)
    if len(sys.argv)>5:
        kind=int(sys.argv[5])
    else:
        kind=3
    main(feature_file,labels_file,align_file,tagdest,kind)
