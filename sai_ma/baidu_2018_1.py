import sys

line1 = map(int, sys.stdin.readline().strip().split(' '))
line2 = map(int, sys.stdin.readline().strip().split(' '))
n1 = line1[0]
n2 = line2[0]
n1_ary = line1[1:]
n2_ary = line2[1:]

n1_ary.reverse()
n2_ary.reverse()


def count(x):
    return 1.0/x
tmp_1 = n1_ary[0]
if n1 != 0:
    for i in range(n1):
        tmp_1 = count(tmp_1)+n1_ary[i+1]
x = tmp_1 + n1_ary[n1]

tmp_2 = n2_ary[0]
if n2 != 0:
    for i in range(n2):
        tmp_2 = count(tmp_2)+n2_ary[i+1]

y = tmp_2 + n2_ary[n2]

print x, y

