import os

stay_lab_fid={}
with open('labels_0.502_stay') as f:
    line = f.readline()
    while line:
        ary = line.strip().split()
        fid = ary[0]
        label = ary[1]
        if stay_lab_fid.has_key(label):
            stay_lab_fid[label].append(fid)
        else:
            stay_lab_fid[label]=[fid]
        line = f.readline()
cluster_lab_fid={}
with open('labels_cluster2_0.6') as f:
    line = f.readline()
    while line:
        ary = line.strip().split()
        fid = ary[0]
        label = ary[1]
        if cluster_lab_fid.has_key(label):
            cluster_lab_fid[label].append(fid)
        else:
            cluster_lab_fid[label]=[fid]
        line = f.readline()

cluster=0
with open('labels_0.502_merge','w') as w:
    for v in stay_lab_fid.values():
        for fid in v:
            w.write(fid+' '+str(cluster)+'\n')
        cluster+=1
    for v in cluster_lab_fid.values():
        for fid in v:
            w.write(fid+' '+str(cluster)+'\n')
        cluster+=1
print 'all cluster nums:', cluster
