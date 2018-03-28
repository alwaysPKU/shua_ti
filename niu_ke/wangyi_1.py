#coding=utf-8
import sys
line = sys.stdin.readline().split(' ')
l = int(line[0])
r = int(line[1])
last = 0
res = 0
mark = True
for i in xrange(l, r+1):
    if mark:
        for j in xrange(1, l+1):
            while j != 0:
                last += j % 10
                j = j / 10
            # last += j
        mark = False
    else:
        while i != 0:
            last += i % 10
            i = i / 10
        # last += i

    if last % 3 == 0:
        res += 1
    else:
        continue
print res
