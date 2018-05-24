#coding=utf-8
import sys


if __name__ == '__main__':
    line = sys.stdin.readline().strip()
    payload_len = int(line)
    line = sys.stdin.readline().strip()
    length_data = int(line)
    line = sys.stdin.readline().strip()
    data_off = []
    data_length=[]
    while line != 'end':
        ary = line.split(',')
        data_off.append(int(ary[0]))
        data_length.append(int(ary[1]))
        line = sys.stdin.readline().strip()
    last = length_data+data_length[len(data_length)-1]
    if last <= payload_len:
        data_length[len(data_length) - 1]=last
    else:
        data_length[len(data_length) - 1] = payload_len
        last -= payload_len
        while last > payload_len:
            data_off.append(0)
            data_length.append(payload_len)
            last -= payload_len
        data_off.append(0)
        data_length.append(last)
    for i in range(len(data_off)):
        print str(data_off[i])+','+str(data_length[i])