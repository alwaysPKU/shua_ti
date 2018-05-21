import sys,os

if __name__ == '__main__':
    file = 'chongqing_492_list'
    f = open(file)
    lines = f.readlines()
    for line in lines:
        print line.split()