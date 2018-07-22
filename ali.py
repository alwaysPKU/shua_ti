# -*- coding: utf-8 -*-
if __name__ == '__main__':
    n = int(raw_input())
    m = int(raw_input())
    x = raw_input()
    map = []
    for i in range(n):
        line = [int(x) for x in raw_input().split()]
        map.append(list(line))
    dp = [list(x) for x in map]
    last_dp = [list(x) for x in map]
    for k in range(m - 1):
        for i in range(n):
            for j in range(n):
                tmp = [last_dp[i][x] + map[x][j] for x in range(n) if x != i and x != j]
                dp[i][j] = min(tmp)
        last_dp = [list(x) for x in dp]
    #print dp
    for lst in dp:
        print(' '.join([str(x) for x in lst]))
