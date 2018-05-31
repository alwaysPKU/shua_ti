import os
import numpy as np

label_fid={}
with open('labels_0.502_merge') as f:
    line = f.readline()
    while line:
        ary = line.strip().split()
        fid = ary[0]
        label = ary[1]
        if label_fid.has_key(label):
            label_fid[label].append(fid)
        else:
            label_fid[label]=[fid]
        line = f.readline()
print 'jiao yan cluster nums:', len(label_fid)
fid_params={}
with open('result/shoptest_qualityall_lst') as f:
    line = f.readline()
    while line:
        ary1 = line.strip().split(' ')
        fid = ary1[0]
        if ary1[1].split(',')[1]=='None':
            params = [0.0,0.0]
        else:
            params = map(float, ary1[1].split(',')[:2])
        fid_params[fid]=params
        line=f.readline()
print 'jiao yan samples:', len(fid_params)
if not os.path.exists('result_3'):
    os.mkdir('result_3')
for fids in label_fid.values():
    num = len(fids)
    if num == 1:
        first = str(num).zfill(5)
        file_name=first+'_'+fids[0].rstrip('.jpg')+'.txt'
        with open('result_3/'+file_name,'w') as w:
            w.write(fids[0].rstrip('.jpg')+'\n')
    else:
        daibiao=fids[0]
        score=0
        for fid in fids:
            param=fid_params[fid]
            tmp = param[0]*param[1]
            if tmp > score:
                daibiao=fid
                score=tmp
            else:
              continue
        first = str(num).zfill(5)
        file_name=first+'_'+daibiao.rstrip('.jpg')+'.txt'
        with open('result_3/'+file_name,'w') as w:
            for fid in fids:
                w.write(fid.rstrip('.jpg')+'\n')

 
