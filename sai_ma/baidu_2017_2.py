import sys

colums = int(sys.stdin.readline().strip())


def count(n, a_arry):
    res = 0
    higher = -1
    for i in xrange(n):
        if a_arry[i] > higher:
            res += 1
            higher = a_arry[i]
    return res

res = []
for i in xrange(colums):
    n = int(sys.stdin.readline().strip())
    a_arry = map(int, sys.stdin.readline().strip().split(' '))
    res.append(count(n, a_arry))

for i in res:
    print i
