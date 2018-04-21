import numpy as np
import os
from sklearn.cluster import AgglomerativeClustering
from sklearn.preprocessing import normalize

command = "awk 'sub($1,'idontkonw')' ./data_set/zhangwei_featlst_test_100"
lines = os.popen(command).read()
features = normalize(np.fromstring(lines, 'f', -1, ' ').reshape((-1, 384)))
print(features[0].shape)

# cluster = AgglomerativeClustering(n_clusters=2, affinity='cosine', linkage='average')
# cluster.fit(features)
# command2 = "awk '{print $1}' ./data_set/chongqing_test"
# names_list = os.popen(command2).read()
#
# w = open('./labels_average_1', 'w')
# for id, label in zip(names_list.splitlines(), cluster.labels_):
#     w.write(str(id+' '+str(label)+'\n'))
# w.close()
