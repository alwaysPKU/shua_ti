import numpy as np
import os


def get_ANN_from_file():
    a = range(10000)
    # print a
    lines = os.popen('cat ./data_set/output_file*').read()
    mat = np.fromstring(lines, 'f', -1, ' ').reshape(-1, 3)
    index1 = mat[:, 0].astype('int32')
    print index1[0]
    print type(index1[0])
    index2 = mat[:, 1].astype('int32')
    dists = mat[:, 2].astype('f')
    wh = np.where(dists < 0.65)
    print wh
    # ret = [labels[index1[wh]], labels[index2[wh]], dists[wh], index1[wh], index2[wh]]
    ret = [dists[wh], index1[wh], index2[wh]]
    print a[index1[wh][0]]
    return ret

if __name__ == '__main__':
    res= get_ANN_from_file()
    for i in zip(*res):
        print i
        break

