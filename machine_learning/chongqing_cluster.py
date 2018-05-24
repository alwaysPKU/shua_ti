import numpy as np
import os,sys
from sklearn.cluster import AgglomerativeClustering
from sklearn.preprocessing import normalize


feature_file = sys.argv[1]
features = normalize(np.load(feature_file))
cluster = AgglomerativeClustering(n_clusters=2, affinity='cosine', linkage='average')
cluster.fit(features)
command2 = "awk '{print $1}' ./data_set/chongqing_test"
names_list = os.popen(command2).read()

w = open('./labels_average_1', 'w')
for id, label in zip(names_list.splitlines(), cluster.labels_):
    w.write(str(id+' '+str(label)+'\n'))
w.close()
