#coding=utf-8
import sys
def judge(cash):
    duoyu=cash-5000
    if duoyu < 0:
        shui=0
    elif duoyu<=3000:
        shui=round(duoyu*0.03)
    elif duoyu>3000 and duoyu<=12000:
        shui=round(3000*3/100+(duoyu-3000)*0.1)
    elif duoyu>12000 and duoyu<=25000:
        shui = round(3000 * 0.03 + (12000 - 3000) * 0.1 + (duoyu-12000)+0.2)
    elif duoyu>25000 and duoyu<=35000:
        shui=round(3000 * 0.03 + (12000 - 3000) * 0.1 + (25000-12000)*0.2+(duoyu-25000)*0.25)
    elif duoyu>35000 and duoyu<=55000:
        shui = round(3000 * 0.03 + (12000 - 3000) * 0.1 + (25000 - 12000) * 0.2 + (35000 - 25000) * 0.25 +(duoyu-35000)* 0.3)
    elif duoyu>55000 and duoyu<=80000:
        shui = round(3000 * 0.03 + (12000 - 3000) * 0.1 + (25000 - 12000) * 0.2 + (35000 - 25000) * 0.25 + (55000 - 35000) * 0.3 + (duoyu-55000)*0.35)
    else :
        shui = round(3000 * 0.03 + (12000 - 3000) * 0.1 + (25000 - 12000) * 0.2 + (35000 - 25000) * 0.25 + (55000 - 35000) * 0.3 + (80000 - 55000) * 0.35 + (duoyu-80000)*0.45)
    return shui

if __name__ == '__main__':
    num=int(sys.stdin.readline().strip())
    res=[]
    for i in range(num):
        sal=int(sys.stdin.readline().strip())
        res.append(int(judge(sal)))
    for i in res:
        print i


