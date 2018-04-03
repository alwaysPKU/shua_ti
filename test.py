import numpy as np
import sys, os
#
# a = list(range(21))
# b = np.reshape(a, (7, 3))
# colum1 = b[:, 0].astype('int32')
# row1 = b[0, :].astype('int32')
# th = 3
# print(colum1)
# wh = np.where(colum1 > th)
# print(wh)

# f = open('./source_data/test', 'w')
# for i in range(12):
#     print(str(i)+' '+str(i+1)+' '+str(0.23232), file=f)
imglist = os.popen("awk '{print $1}' " + sys.argv[1]).read().splitlines()
print(imglist)