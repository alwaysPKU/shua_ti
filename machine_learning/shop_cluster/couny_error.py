import sys
import numpy as np
#file_name = sys.argv[1]
#clusters = set()
#with open(file_name) as f:
#    line = f.readline().strip()
#    while line:
#        clusters.add(line.split(' ')[0])
#        line = f.readline().strip()
#print len(clusters)
file_name=sys.argv[1]
file2=sys.argv[2]
clusters={}
last=''
num = 0
all_nums=1690486
with open(file_name) as f:
    lines = f.readlines()
    lines.sort(key=lambda x: x.strip().split(' ')[1])
    for line in lines:
        num+=1
        arry = line.strip().split(' ')
        this = arry[1]
        if last == '' or last != this:
            clusters[this]=1
            last=this
        else:
            clusters[this]+=1
print '###########################################'
print 'input:',file_name, '   ',file2
num_clusters=len(clusters)
print 'nums of clusters:', num_clusters
print 'nums of samples:', num
print 'nums of filted data:',str(all_nums-num),'  rate:%5.2f%%'%((all_nums-num)/float(all_nums)*100)

i_1=0
img_1=0
i_2_9=0
img_2_9=0
i_10_50=0
img_10_50=0
i_50_200=0
img_50_200=0
i_200_500=0
img_200_500=0
i_500_2000=0
img_500_2000=0
i_2000_5000=0
img_2000_5000=0
i_5000=0
img_5000=0
for v in clusters.values():
    if v==1:
        i_1+=1
        img_1+=v
    elif v>=2 and v<10:
        i_2_9+=1
        img_2_9+=v
    elif v>=10 and v<50:
        i_10_50+=1
        img_10_50+=v
    elif v>=50 and v<200:
        i_50_200+=1
        img_50_200+=v
    elif v>=200 and v<500:
        i_200_500+=1
        img_200_500+=v
    elif v>=500 and v<2000:
        i_500_2000+=1
        img_500_2000+=v
    elif v>=2000 and v<5000:
        i_2000_5000+=1
        img_2000_5000+=v
    else:
        i_5000+=1
        img_5000+=v
num1 = img_1/float(num)*100
num2 = img_2_9/float(num)*100
num3 = img_10_50/float(num)*100
num4 = img_50_200/float(num)*100
num5 = img_200_500/float(num)*100
num6 = img_500_2000/float(num)*100
num7 = img_2000_5000/float(num)*100
num8 = img_5000/float(num)*100
print '=======================samples distribute====================='
print 'samples=1:          %7d'%i_1,'%8d'%img_1,'%8.2f %%'%num1
print 'samples=[2,9):      %7d'%i_2_9,'%8d'%img_2_9,'%8.2f %%'%num2
print 'samples=[10,50):    %7d' %i_10_50,'%8d'%img_10_50,'%8.2f %%'%num3
print 'samples=[50,200):   %7d'%i_50_200,'%8d'%img_50_200,'%8.2f %%'%num4
print 'samples=[200,500):  %7d'%i_200_500,'%8d'%img_200_500,'%8.2f %%'%num5
print 'samples=[500,2000): %7d'%i_500_2000,'%8d'%img_500_2000,'%8.2f %%'%num6
print 'samples=[2000,5000):%7d'%i_2000_5000,'%8d'%img_2000_5000,'%8.2f %%'%num7
print 'samples>=5000:      %7d'%i_5000,'%8d'%img_5000,'%8.2f %%'%num8
print 'effctive data: %8.2f %%'%(100-num1-num2)
print '=======================variance distribute===================='

#file2=sys.argv[2]
mat = np.fromstring(open(file2).read(),'f',-1,' ').reshape(-1,2)
#print mat.shape
variance = mat[:,1]
labels =np.array(map(str,map(int, mat[:,0])))
thr=[0.6,0.65,0.7]
for i in thr:
    num_cluster=len(np.where(variance>i)[0])
    index=np.where(variance>i)[0]
    label_tmp=labels[index]
    num_samples=0
    for label in label_tmp:
        num_samples+=clusters[label]
    print 'variance > %3.2f'%i,'---',' num of clusters:%5d and rate:%5.3f%%'%(num_cluster,num_cluster/float(num_clusters)*100),'---',' num of samples:%7d and rate:%6.3f%%'%(num_samples,num_samples/float(num)*100)
print '=============================================================='
print '###########################################'
print '\n\n'   












