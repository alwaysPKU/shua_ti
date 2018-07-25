# -*- coding:utf-8 -*-
class Solution:
    def jumpFloor(self, number):
        res=[0,1,2]
        if number<3:
            return res[number]
        first = 1
        second = 2
        for i in range(3,number+1):
            tmp = first+second
            first=second
            second=tmp
        return tmp