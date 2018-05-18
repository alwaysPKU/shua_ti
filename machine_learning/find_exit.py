import os,sys

file = 'chongqing_492_list'
path = os.popen("awk '{print$1}' " + file).read().splitlines()
num = 0
for i in path:
    if os.path.exists(i):
        num+=1
        continue
    else:
        print i
print num