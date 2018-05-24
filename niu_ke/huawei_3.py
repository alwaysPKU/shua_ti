#coding=utf-8
import sys


def byte(st):
    if st == 'unsigned char' or st == 'char' :
        return 1
    elif st == 'short' or st == 'unsigned short':
        return 2
    elif st == 'int' or st == 'unsigned int' or st == 'long' or st == 'unsigned long':
        return 4
    else:
        return 0


def get_num(num):
    ary = num.split('][')
    if len(ary)==1:
        return int(num.split('[')[-1].rstrip(']'))
    else:
        length = len(ary)
        ans = 1
        for i in range(length):
            if i==0:
                ans *= int(ary[0].split('[')[-1])
            elif i == length-1:
                ans *= int(ary[i].split(']')[0])
            else:
                ans*=int(ary[i])
        return ans
if __name__ == '__main__':
    line = sys.stdin.readline().strip().rstrip(';')
    ary = line.split()
    st = ''
    for i in ary[:-1]:
        st = st+i+' '
    st = st.rstrip(' ')
    # num = int(ary[-1].split('[')[-1].rstrip(']'))
    num = get_num(ary[-1])
    by = byte(st)
    print by*num
