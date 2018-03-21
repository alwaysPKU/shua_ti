import sys


store = map(int, raw_input().split(' '))
num = store[0]
operation_num = store[1]
arry = []
for i in range(num):
    arry.append(int(raw_input()))


def operation(operation_num):
    res = []
    for i in range(operation_num):
        opertaion = map(int, raw_input().strip(' ').split(' '))
        if opertaion[0] == 1:
            arry[opertaion[1]-1] = opertaion[2]
        elif opertaion[0] == 2:
            tmp = 0
            for j in range(opertaion[1]-1, opertaion[2]):
                tmp += arry[j]
            res.append(tmp)
        elif opertaion[0] == 3:
            tmp = arry[opertaion[1]-1]
            for j in range(opertaion[1]-1, opertaion[2]):
                if tmp < arry[j]:
                    tmp = arry[j]
                else:
                    continue
            res.append(tmp)
    return res

res = operation(operation_num)
for i in res:
    sys.stdout.write(str(i)+'\n')
