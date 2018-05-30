from scipy.spatial.distance import cdist
import numpy as np

a = np.array([[1,2,3],[1, 1, 1],[1,2,3],[1, 1, 1]]          )
b = np.array([[1,2,3],[1,2,3]])
print b
c = cdist(a,b)
print c
index=np.where(c>0.)
print index

a=[1,2,3]
b = [1,4,1]
c= a[:1]+[a[1]]
print c