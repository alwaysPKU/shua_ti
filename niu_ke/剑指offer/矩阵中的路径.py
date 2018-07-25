# -*- coding:utf-8 -*-
class Solution:
    def hasPath(self, matrix, rows, cols, path):
        # write code here
        if not matrix or rows<1 or cols<1 or not path:
            return False
        not_visited= [range(1,cols+1)]*rows
        for i in range(rows):
            for j in range(cols):
                if self.judge(matrix,rows,cols,i,j,path,0,not_visited):
                    return True
        return False
    def judge(self,matrix,rows,cols,row,col,path,num,not_visited):
        if num==len(path)-1:
            return True
        jud=False
        if row>=0 and row < rows and col>=0 and col<=cols and matrix[row][col]==path[num] and not_visited[row][col]:
            num+=1
            not_visited[row][col]=0
            jud=self.judge(matrix,rows,cols,row,col-1,path,num,not_visited) or self.judge(matrix,rows,cols,row-1,col,path,num,not_visited) or self.judge(matrix,rows,cols,row,col+1,path,num,not_visited) or self.judge(matrix,rows,cols,row+1,col,path,num,not_visited)
            if not jud:
                num-=1
                not_visited[row][col]=1
        return jud

s=Solution()
print s.hasPath()