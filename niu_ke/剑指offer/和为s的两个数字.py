# -*- coding:utf-8 -*-
class Solution:
    def FindNumbersWithSum(self, array, tsum):
        for i in range(len(array)-1):
            for j in range(i+1, len(array)):
                if array[i] + array[j] == tsum:
                    return [array[i],array[j]]
        return []
    # write code here

test = Solution()
a = test.FindNumbersWithSum([1,2,4,7,11,15],15)
print a