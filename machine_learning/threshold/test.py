import numpy as np
from ctypes import *

calc=CDLL('libthreshold.so')
calc.calcthreshold.argtypes=[]

a=np.load('output_file_0.5.npy')
# a= np.array(a)
# print a
print a[:,0],a[:,1],a[:,2]

