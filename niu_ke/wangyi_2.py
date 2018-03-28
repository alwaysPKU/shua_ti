#coding=utf-8
import sys


def find_index(ary_di, di):
    start = 0
    end = n-1
    mid = 0
    while start < end-1:
        mid = (end + start) / 2
        if ary_di[mid] > di:
            end = mid
        elif ary_di[mid] < di:
            start = mid
        else:
            return mid
    if ary_di[start] > di:
        return start
    if ary_di[end] < di:
        return end
    return end
if __name__ == '__main__':
    line1 = sys.stdin.readline().split(' ')
    n = int(line1[0])
    m = int(line1[1])
    ary_di = []
    ary_pi = []
    for i in range(n):
        line = sys.stdin.readline().strip()
        values = map(int, line.split(' '))
        ary_di.append(values[0])
        ary_pi.append(values[1])
    line = sys.stdin.readline().strip()
    job = map(int, line.split(' '))

    for i in job:
        index = find_index(ary_di, i)
        print ary_pi[index]
