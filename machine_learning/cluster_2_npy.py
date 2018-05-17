import sys, os
import numpy as np
# from sklearn.preprocessing import normalize
from pyflann import FLANN
import datetime


def get_id_time(fid):
    id, time = '', ''
    key = fid.split('/')[-1].rstrip('.jpg')
    ary = key.split('_')
    if len(ary) == 6:
        id = ary[0] + ary[1]
        time = ary[2]
    else:
        ary = key.split('-')
        id = ary[0] + ary[1]
        tmp = ary[2].split('_')
        time = '20' + tmp[0] + tmp[1]
    return id, time


def get_idtime_key(fid):
    id, time = '', ''
    key = fid.split('/')[-1].rstrip('.jpg')
    ary = key.split('_')
    if len(ary) == 6:
        id_time = ary[0] + ary[1] + ary[2]
    else:
        id_time = ary[0] + ary[1]
    return id_time


def time_window(l_fid, r_fid, fids):
    '''
    if the two pics in the time_window = 1minute
    :param l_fid:
    :param r_fid:
    :return: boolean
    '''
    l = fids[l_fid]
    r = fids[r_fid]
    l_id, l_time = get_id_time(l)
    r_id, r_time = get_id_time(r)
    if l_id == r_id :
        d1 = datetime.datetime.strptime(l_time, '%Y%m%d%H%M%S%f')
        d2 = datetime.datetime.strptime(r_time, '%Y%m%d%H%M%S%f')
        delta = abs(d1 - d2)
        if delta.total_seconds() <= time_threshold:
            return True
    return False


def read(fid_label_file): #fid_features_file
    '''
    read file
    :param fid_label_file: 
    :param fid_features_file: 
    :return: fid[],labels[],features[[]],label_index{label:[index1,index2...]}
    '''
    t1 = datetime.datetime.now()
    print 'start read:' , t1
    label_index_dict = {}
    fids = []
    labels = []
    # fids = os.popen("awk '{print $1}' " + fid_label_file).read().strip().splitlines()
    # labels = os.popen("awk '{print $2}' " + fid_label_file).read().strip().splitlines()
    with open(fid_label_file) as f:
        line = f.readline()
        i = 0
        while line:
            ary = line.strip().split(' ')
            fids.append(ary[0])
            labels.append(ary[1])
            if not label_index_dict.has_key(ary[1]):
                label_index_dict[ary[1]]=[]
            label_index_dict[ary[1]].append(i)
            i+=1
            line = f.readline()
    # lines = os.popen("awk 'sub($1,'idontknow')' "+fid_features_file).read()
    # features = normalize(np.fromstring(lines, 'f', -1, ' ').reshape(-1, 384))
    #features = normalize(np.loadtxt(fid_features_file, usecols=range(1, 385)))
    #print features.shape
    t2 = datetime.datetime.now()
    print 'end read:', t2, t2-t1,'\n'
    return np.array(fids), np.array(labels),label_index_dict# np.array(features), label_index_dict


def write(fids, new_labels, out_put):
    '''
    output
    :param fids: fid
    :param new_labels: label
    :param out_put: file_name
    :return: 
    '''
    t1 = datetime.datetime.now()
    print 'start write:' , t1
    with open(out_put, 'w') as w:
        for fid, label in zip(fids, new_labels):
            w.write(fid+' '+str(label)+'\n')
    t2 = datetime.datetime.now()
    print 'end write:', t2, t2-t1, '\n'


def get_ANN(features, labels):
    '''
    100 nearest
    :param features: 
    :param labels: 
    :param fid: no.......................
    :return: [[l_label],[r_label],[dist],[l_index],[r_index]]
    '''
    flann = FLANN()
    K = 100
    results, dists = flann.nn(features, features, K,)
    index = np.tile(np.arange(results.shape[0]).reshape(-1, 1), results.shape[1])
    not_same = labels[results] != labels[index]
    threshold = dists < 0.7  # ou shi juli de pingfang
    wh = np.where(not_same & threshold)
    print len(wh[0])
    ret = [labels[wh[0]], labels[results[wh]]]
    Dist = [dists[wh]]
    index1 = [wh[0]]
    index2 = [results[wh]]
    return ret+Dist+index1+index2


def get_ANN_from_file(labels):
    '''
    output_file
    :param labels: 
    :return: [[l_label],[r_label],[dist],[l_index],[r_index]]
    '''
    t1 = datetime.datetime.now()
    print 'start get dist from output:', t1
   # lines = os.popen('cat output_file*').read()
   # mat = np.fromstring(lines, 'f', -1, ' ').reshape(-1, 3)
    mat = np.load('./threshold/output_file_0.5.npy')
    index1 = mat[:, 0].astype('int32')
    index2 = mat[:, 1].astype('int32')
    dists = mat[:, 2].astype('f')
    not_same = labels[index1] != labels[index2]
    threshold = dists < 0.7 
    threshold2 = dists > s_c_c_d  # consine dist
    wh = np.where(not_same & threshold & threshold2)
    ret = [labels[index1[wh]], labels[index2[wh]], dists[wh], index1[wh], index2[wh]]
    t2 = datetime.datetime.now()
    print 'end get dist from output:', t2, t2-t1, '\n'
    return ret


def merge_labels(labels_fix):
    '''
    :param labels_fix:[[],[],[],[]] 
    :return: [[],[]]
    '''
    t1 = datetime.datetime.now()
    print 'start merge:', t1
    map_1 = {}
    map_2 = {}
    for i, tumple in enumerate(labels_fix):
        if not map_1.has_key(tumple[0]) and not map_1.has_key(tumple[1]):
            map_1[tumple[0]] = i
            map_1[tumple[1]] = i
            map_2[i] = [tumple[0], tumple[1]]
        elif not map_1.has_key(tumple[0]):
            map_1[tumple[0]] = map_1[tumple[1]]
            map_2[map_1[tumple[1]]].append(tumple[0])
        elif not map_1.has_key(tumple[1]):
            map_1[tumple[1]] = map_1[tumple[0]]
            map_2[map_1[tumple[0]]].append(tumple[1])
        else:
            if map_1[tumple[0]] != map_1[tumple[1]]:
                if len(map_2[map_1[tumple[0]]]) >= len(map_2[map_1[tumple[1]]]):
                    map_2[map_1[tumple[0]]] = map_2[map_1[tumple[0]]] + map_2[map_1[tumple[1]]]
                    tmp = map_1[tumple[1]]
                    for i in map_2[map_1[tumple[1]]]:
                        map_1[i] = map_1[tumple[0]]
                    del map_2[tmp]
                else:
                    map_2[map_1[tumple[1]]] = map_2[map_1[tumple[1]]] + map_2[map_1[tumple[0]]]
                    tmp = map_1[tumple[0]]
                    for i in map_2[map_1[tumple[0]]]:
                        map_1[i] = map_1[tumple[1]]
                    del map_2[tmp]
            else:
                continue
                # for key, values in map_2.items():
                #     print key, values
                # print '================='
    t2 = datetime.datetime.now()
    print 'end merge:', t2, t2-t1, '\n'
    return [i for i in map_2.values()]


def main(fid_label_file,out_put):
    labels_fix = []
    dele_fix = []
    fids, labels, label_indexes = read(fid_label_file)# fid_features_file)
    # results = get_ANN(features, labels)
    results = get_ANN_from_file(labels)
    last_a = ''
    last_b = ''
    new_labels = np.array([-1]*len(labels))

    t1 = datetime.datetime.now()
    print 'start find merge label:', t1
    for a, b, dist, l_index, r_index in sorted(zip(*results)):
        if a == last_a and b == last_b:
            continue
        if time_window(l_index, r_index, fids):
            labels_fix.append([a, b])
            last_a=a
            last_b=b
    t2 = datetime.datetime.now()
    print 'end find merge label:', t2-t1
    print 'len merge label', len(labels_fix)
    # add dele_fix
    tmp_dict = {}
    tmp_set = set()
    for index, img_name in enumerate(fids):
        id_name = get_idtime_key(img_name)
        if tmp_dict.has_key(id_name):
            tmp_set.add(id_name)
            tmp_dict[id_name].append(index)
        else:
            tmp_dict[id_name]=[index]
    for i in tmp_set:
        value = tmp_dict[i]
        num = len(value)
        for j in range(num):
            for k in range(num):
                if k == j or labels[value[j]] == labels[value[k]] or [labels[value[j]], labels[value[k]]] in dele_fix:
                    continue
                else:
                    dele_fix.append([labels[value[j]], labels[value[k]]])

    t3 = datetime.datetime.now()
    print 'len dele label:', len(dele_fix)
    print 'end find dele label:', t3-t2, '\n'
    #print 'tongyizhen:',len(dele_fix)
   # print 'before:',len(labe_fix)
    labels_fix = [v for v in labels_fix if v not in dele_fix]
    print 'after dele merge label:',len(labels_fix)
    res = merge_labels(labels_fix)
    num_cluster = len(res)
    print 'ronghecheng:', num_cluster
    merge_num = 0
    for cluster, i in enumerate(res):
        #print cluster
        merge_num += len(i)
        for j in i:
            for k in label_indexes[j]:
                new_labels[k] = cluster
            del label_indexes[j]
    print '%d cluster merged' % merge_num
    for v in label_indexes.values():
        for i in v:
            new_labels[i] = num_cluster
        num_cluster += 1
    # for i, label in enumerate(new_labels):
    #     if label == -1:
    #         new_labels[i] = num_cluster
    #         num_cluster += 1
    write(fids, new_labels, out_put)

if __name__ == '__main__':
    t1 = datetime.datetime.now()
    print 'start...main', t1, '\n'
   # os.system('./release04_0.55 '+sys.argv[2])
   #  fid_label_file = sys.argv[1]
   #  fid_features_file = sys.argv[2]
   #  out_put = sys.argv[3]
   #  main(fid_label_file, fid_features_file, out_put)
    fid_label_file = ''
    time_threshold = 0.0
    s_c_c_d = 0.0
    out_put = ''
    with open('cluster_2_params') as f:
        line = f.readlines()
        line_1ary=line[0].strip().split(':')
        line_2ary = line[1].strip().split(':')
        line_3ary = line[2].strip().split(':')
        print line_1ary, line_2ary, line_3ary, '\n'
        fid_label_file=line_1ary[1]
        time_threshold = float(line_2ary[1])
        s_c_c_d = float(line_3ary[1])
        print 'in_put:', sys.argv[0]
        out_put = 'labels_'+str(s_c_c_d)+'_0.7_'+str(time_threshold)+'s_by_npy_not_merge'
        print 'out_put:', out_put, '\n'
    main(fid_label_file, out_put)
    t2 = datetime.datetime.now()
    print 'end...main', t2 , t2-t1, '\n'
