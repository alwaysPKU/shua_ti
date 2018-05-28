import sys


row = int(sys.stdin.readline().strip())
col = int(sys.stdin.readline().strip())

mat = []
for i in range(row):
    line = sys.stdin.readline().strip('\n').split()
    line = map(int, line)
    mat.append(line)

# mark=[]
# for i in range(col):
#     mark.append([0]*row)


ans=0
def compute_bingli(i,j,ans):
    if mat[i][j] == 0:
        return
    else:
        ans+=mat[i][j]



