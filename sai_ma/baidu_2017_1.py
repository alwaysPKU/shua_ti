import sys


def count(line):
    line_ary = line.split(' ')
    name = line_ary[0]
    a = int(line_ary[1])
    b = int(line_ary[2])
    c = line_ary[3]
    d = line_ary[4]
    x = int(line_ary[5])
    res = 0
    if a > 80 and x >= 1:
        res += 8000
    if a > 85 and b > 80:
        res += 4000
    if a > 90:
        res += 2000
    if a > 85 and d == 'Y':
        res += 1000
    if b > 80 and c == 'Y':
        res += 850
    return name, res

N = int(sys.stdin.readline().strip())

name_max = ''
max_ = 0
counts = 0
for i in range(N):
    line = sys.stdin.readline().strip()
    name, res = count(line)
    counts += res
    if max_ < res:
        name_max = name
        max_ = res
print name_max
print max_
print counts

