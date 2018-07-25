# -*- coding:utf-8 -*-
import sys
if __name__ == '__main__':
    line_ary=map(int, sys.stdin.readline().strip().split(' '))
    n=line_ary[0]
    k=line_ary[1]
    num=sys.stdin.readline().strip()
    num2=map(int,[num[i] for i in range(n)])
    dic={}
    for i in num2:
        if i in dic:
            dic[i]+=1
        else:
            dic[i]=1
    print dic
    tmp = sorted(dic.items(),key=lambda x:(x[1],x[0]))
    print tmp
    dic_find={}
    if tmp[-1][1]>=k:
        print 0
        print num
    else:
        sums=0
        numbers=0
        for l,r in tmp:
            sums=sums+l*r
            numbers+=r
        average=sums/numbers
        if sums%numbers*2>=average:
            average+=1











