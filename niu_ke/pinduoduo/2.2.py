# -*- coding:utf-8 -*-
import sys
import math
if __name__ == '__main__':
    s=sys.stdin.readline().strip()
    # print s
    length=len(s)
    for i in range(1,length+1):
        if length%i==0:
            # print i
            p=s[:i]
            num=0
            for j in range(length):
                if s[j]==p[j%i]:
                    num+=1
                    continue
                else:
                    break
            if num==length:
                print p
                break
