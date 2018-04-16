import numpy as np
import os
from sklearn.cluster import AgglomerativeClustering
from sklearn.preprocessing import normalize

command = "awk 'sub($1,'idontkonw')' ./data_set/chongqing_test"
lines = os.popen(command).read()
features = normalize(np.fromstring(lines, 'f', -1, ' ').reshape((-1, 384)))
print(features.shape)

cluster = AgglomerativeClustering(n_clusters=2, affinity='cosine', linkage='average')
cluster.fit(features)
command2 = "awk '{print $1}' ./data_set/chongqing_test"
names_list = os.popen(command2).read()

w = open('./labels_average', 'w')
for id, label in zip(names_list.splitlines(), cluster.fit_predict(features)):
    w.write(str(id+' '+str(label)+'\n'))
w.close()
