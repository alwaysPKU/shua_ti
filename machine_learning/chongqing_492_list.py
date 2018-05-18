import  re
import sys

if __name__ == '__main__':
    file_para = sys.argv[1]
    f = open(file_para)
    w = open('./chongqing_492_list', 'w')

    line = f.readline()
    while line:
        pattern = re.compile(r'"\[.*]"')
        obj = pattern.search(line)
        if obj:
            fid = line.split(',')[2]
            lmk =  obj.group().lstrip('"[').rstrip(']"')
            w.write('./'+fid+' '+'-1'+' '+lmk+'\n')
        line = f.readline()
    w.close()
    f.close()

