import sys
n = int(raw_input())
ary = map(int, raw_input().split(' '))
ary.sort()


def solution(n, ary):
    count = 1
    res = 0
    if n == 0:
        return 3
    if n == 1:
        return 2
    for index in range(1, n):
        if count == 1:
            if ary[index]-ary[index-1] <= 10:
                count += 1
            elif ary[index]-ary[index-1] <= 20:
                count += 1
                res += 1
            elif ary[index]-ary[index-1] > 20:
                res += 2
                count += 2
                if count == 3:
                    count = 1
        elif count == 2:
            if ary[index]-ary[index-1] <= 10:
                count += 1
            elif ary[index]-ary[index-1] > 10:
                res += 1
                count += 1
                if count == 3:
                    count = 1
        elif count == 3:
            count = 1
    return res + 3 - count


def solution2(n, ary):
    res = 0
    num = 0
    for x in ary:
        num %= 3
        if num != 0 and x > last + 10:
            res += 3 - num
            num = 0
        num += 1
        last = x
    return res


res = solution(n, ary)
sys.stdout.write(str(res))
