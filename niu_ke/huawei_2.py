#coding=utf-8
import sys


if __name__ == '__main__':
    num = sys.stdin.readline().strip()
    num_ary = map(int, num.split())
    num_ary = list(set(num_ary))
    num_ary.sort()
    # print num_ary
    ans = num_ary[0] * num_ary[0] + (num_ary[0] + num_ary[0]) * (num_ary[0] - num_ary[0]) + num_ary[0]
    length = len(num_ary)
    # print length
    for i in range(length):
        for j in range(i+1, length):
            # print i,j
            # k = num_ary[length-1]
            # tmp = num_ary[i]**2+num_ary[i]*num_ary[j]-num_ary[j]**2+num_ary[length-1]
            tmp = num_ary[i]*num_ary[j]+(num_ary[i]+num_ary[j])*(num_ary[i]-num_ary[j])+num_ary[0]
            if tmp < ans:
                # print i,j
                ans = tmp
    print ans