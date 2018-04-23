import sys, os
import numpy as np
from sklearn.preprocessing import normalize
from pyflann import FLANN
import datetime


def get_id_time(fid):
    id, time = '', ''
    key = fid.split('/')[-1].rstrip('.jpg')
    ary = key.split('_')
    if len(ary) == 6:
        id = ary[0] + ary[1]
        time = ary[2][:-3]
    else:
        ary = key.split('-')
        id = ary[0] + ary[1]
        tmp = ary[2].split('_')
        time = '20' + tmp[0] + tmp[1]
    return id, time


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
        d1 = datetime.datetime.strptime(l_time, '%Y%m%d%H%M%S')
        d2 = datetime.datetime.strptime(r_time, '%Y%m%d%H%M%S')
        delta = d1 - d2
        if abs(delta.seconds) <= 60:
            return True
    return False


def read(fid_label_file, fid_features_file):
    '''
    read file
    :param fid_label_file: 
    :param fid_features_file: 
    :return: fid[],labels[],features[[]],label_index{label:[index1,index2...]}
    '''
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
    features = normalize(np.loadtxt(fid_features_file, usecols=range(1, 385)))
    print features.shape
    return np.array(fids), np.array(labels), np.array(features), label_index_dict


def write(fids, new_labels, out_put):
    '''
    output
    :param fids: fid
    :param new_labels: label
    :param out_put: file_name
    :return: 
    '''
    with open(out_put, 'w') as w:
        for fid, label in zip(fids, new_labels):
            w.write(fid+' '+str(label)+'\n')


def get_ANN(features, labels):
    '''
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
    threshold = dists < 0.7
    wh = np.where(not_same & threshold)
    print len(wh[0])
    ret = [labels[wh[0]], labels[results[wh]]]
    Dist = [dists[wh]]
    index1 = [wh[0]]
    index2 = [results[wh]]
    return ret+Dist+index1+index2


def merge_labels(labels_fix):
    '''
    :param labels_fix:[[],[],[],[]] 
    :return: [[],[]]
    '''
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
    return [i for i in map_2.values()]


def main(fid_label_file, fid_features_file,out_put):
    labels_fix = []
    fids, labels, features, label_indexes = read(fid_label_file, fid_features_file)
    results = get_ANN(features, labels)
    last_a = ''
    last_b = ''
    new_labels = np.array([-1]*len(labels))
    for a, b, dist, l_index, r_index in sorted(zip(*results)):
        if a == last_a and b == last_b:
            continue
        if time_window(l_index, r_index, fids):
            labels_fix.append([a, b])
        last_a=a
        last_b=b
    res = merge_labels(labels_fix)
    num_cluster = len(res)
    merge_num = 0
    for cluster, i in enumerate(res):
        print cluster
        merge_num += len(i)
        for j in i:
            for k in label_indexes[j]:
                new_labels[k] = cluster
    print '%d cluster merged'
    for i, label in enumerate(new_labels):
        if label == -1:
            new_labels[i] = num_cluster
            num_cluster += 1
    write(fids, new_labels, out_put)

if __name__ == '__main__':
    print datetime.time()
    fid_label_file = sys.argv[1]
    fid_features_file = sys.argv[2]
    out_put = sys.argv[3]
    main(fid_label_file, fid_features_file, out_put)
    print datetime.time()
