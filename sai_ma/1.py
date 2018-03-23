import sys

s = raw_input().strip()
t = raw_input().strip()


def distance(a, b):
    dis = 0
    for i in range(len(a)):
        if a[i] != b[i]:
            dis += 1
        else:
            continue
    return dis
num = len(s) - len(t)
res = 0
for i in range(num+1):
    res += distance(s[i:i+len(t)], t)
sys.stdout.write(str(res))
