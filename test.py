from pyflann import *
import numpy as np
from sklearn.preprocessing import normalize
dataset = normalize(np.array(
    [[1., 1, 1, 2, 3, 1, 1, 1, 2, 3],
     [10, 10, 10, 3, 2, 1, 1, 1, 2, 3],
     [100, 100, 2, 30, 1, 1, 1, 1, 2, 3],
     [1, 11, 11, 2, 3, 1, 1, 1, 2, 3],
     [10, 101, 101, 3, 2, 1, 1, 1, 2, 3],
     [100, 100, 211, 30, 11, 1, 1, 1, 2, 3]
     ]))
testset = np.array(
    [[1., 1, 1, 1, 1],
     [90, 90, 10, 10, 1]
     ])
flann = FLANN()
result, dists = flann.nn(
    dataset, dataset, 6, algorithm="kdtree")
print result
print dists
print np.tile(np.arange(3).reshape(-1,1), 3)
print '====================================='
label = np.arange(100,step=2)
ind = np.arange(10).reshape(2, 5)
print label[ind]

print '============wh' \
      '==============='
a= array([1, 2, 3, 1, 2, 3, 1, 2, 3]).reshape(3,3)
print a
wh = np.where(a>2)
print wh
print 'wh[0]:',wh[0]
print 'wh[1]:',wh[1]
print 'a[wh]:',a[wh]
ret= [wh[0], a[wh]]
print ret
result = ret + [[1,2,3]]
print result
for i,j,k in zip(*result):
    print i,j,k



print '==========='

aa = np.arange(100)
tiaojian = np.array([[0,1,3,5,2,4],
 [1,5,3,4,2,0]])
res = aa[tiaojian]
print res

print '======len======='
l = [1,2,3,4,5]
for i in l[:9]:
    print i

