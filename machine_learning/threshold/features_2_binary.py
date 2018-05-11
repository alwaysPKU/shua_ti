import numpy as np
import sys


def read(f):
    mat = np.loadtxt(f,dtype=np.float32, usecols=range(1,385))
    print type(mat)
    return mat

if __name__ == '__main__':
    file = 'zhangwei_featlst_10001'
    mat = read(file)
    np.save('zhangwei_featlst_binary', mat)

mat = np.load('zhangwei_featlst_binary.npy')
print mat.shape
print type(mat[0,1])