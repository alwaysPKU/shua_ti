# -*- coding:utf-8 -*-
class Solution:
    def Fibonacci(self, n):
        res=[0,1]
        first=0
        second=1
        if n<2:
            return res[n]
        for i in range(2,n+1):
            tmp=first+second
            first=second
            second=tmp
        return tmp
s=Solution()
print s.Fibonacci(39)
