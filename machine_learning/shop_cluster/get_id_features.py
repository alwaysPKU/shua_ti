import numpy as np
import os


a = np.fromstring(open('label_varience').read(), 'f', -1 ,' ').reshape(-1 ,2)
b = a[:,1]
label =np.array(os.popen("awk '{print$1}' label_varience").read().splitlines())
print label.shape
need_split_label=label[np.where(b>0.45)]
need_stay_label=label[np.where(b<=0.45)]
print 'how many cluster need split:', len(need_split_label)
label_id={}
fid_labels={}
with open('labels_0.502') as f:
    line = f.readline().strip()
    while line:
        ary = line.split()
        fid = ary[0]
        label = ary[1]
        fid_labels[fid]=line
        if label_id.has_key(label):
            label_id[label].append(fid)
        else:
            label_id[label]=[fid]
        line = f.readline().strip()
print 'jiao yan cluster num:', len(label_id)
fid_features={}
with open('result/shoptest_featuresall_lst') as f:
    line = f.readline()
    while line:
        ary = line.split(' ')
        fid = ary[0]
        fid_features[fid]=line
        line = f.readline()
print 'jiao yan samples nums:', len(fid_features)
num = 0
num2 = 0
with open('shop_new_feature_0.45','w') as w:
    for label in need_split_label:
        for fid in label_id[label]:
            num+=1
            w.write(fid_features[fid])
print 'how many samples need cluster again:', num
with open('labels_0.502_stay','w') as w:
    for label in need_stay_label:
        for fid in label_id[label]:
            num2+=1
            w.write(fid_labels[fid]+'\n')
print 'how many samples stay:', num2
