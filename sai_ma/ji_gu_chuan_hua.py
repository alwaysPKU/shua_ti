import sys


def solution(n, m):
    dp = [[0]*(31) for i in range(31)]
    dp[1][1] = 1
    dp[1][n-1] = 1
    for i in range(2, m+1):
        for j in range(0, n):
            dp[i][j] = dp[i - 1][(n-j-1) % n] + dp[i - 1][(n-j+1) % n]
    return dp[m][0]
num = raw_input().strip().split(' ')
n = int(num[0])
m = int(num[1])
sys.stdout.write(str(solution(n, m)))
