import numpy as np
a = [[1,2],[2,3]]
b = [[1,2]]
c = [[1,2]]

a =  [v for v in a if v not in b]
print a