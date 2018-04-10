import sys
Step = int(sys.stdin.readline())
line2 = map(int, sys.stdin.readline().split(' '))
X = line2[0]
Y = line2[1]

def dp(x, y,step, X, Y, Step, res):
    if x == X and y == Y and step == Step:
        res += 1
        return
    elif x > X or y > Y or step > Step:
        return
    elif x < X and step < Step and y < Y:
        x += 1
        y += 2
        step += 1
        dp(x, y, step, X, Y, Step, res)
        x -= 1
        y -= 2
        step -= 1
        x += 2
        y += 1
        step += 1
        dp(x, y, step, X, Y, Step, res)
        x -= 1
        y -= 2
        step -= 1


if __name__ == '__main__':
    res = 0
    x = 0
    y = 0
    step = 0
    dp(x, y, step, X, Y, Step, res)
    print res
