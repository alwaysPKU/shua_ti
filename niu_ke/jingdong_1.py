import sys


t = int(sys.stdin.readline().strip())


def pan_ding(n):
    if oushu_panding(n):
        for y in xrange(2, n+1, 2):
            x = n/y
            t = n % y
            if jishu_panding(x) and t == 0:
                return x, y
            else:
                continue
    return 'No'


def jishu_panding(n):
    if n % 2 == 1:
        return True
    else:
        return False


def oushu_panding(n):
    if n % 2 == 0:
        return True
    else:
        return False


con = []
for i in xrange(t):
    n = int(sys.stdin.readline())
    con.append(n)

for i in con:
    res = pan_ding(i)
    if res != 'No':
        print res[0], res[1]
    else:
        print res
