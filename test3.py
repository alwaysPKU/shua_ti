import datetime, time
path = './machine_learning/data_set/fid_test'
fids = []
with open(path) as f:
    lines = f.readlines()
    for line in lines:
        ary = line.strip().split(' ')
        fids.append(ary[0])
for fid in fids:
    print fid
    id, time = '', ''
    key = fid.split('/')[-1].rstrip('.jpg')
    ary = key.split('_')
    if len(ary) == 6:
        id = ary[0]+ary[1]
        time = ary[2][:-3]
    else:
        ary = key.split('-')
        id = ary[0]+ary[1]
        tmp = ary[2].split('_')
        time = '20'+tmp[0]+tmp[1]
    print id, time

def dele_time(l ,r):
    d1 = datetime.datetime.strptime(l, '%Y%m%d%H%M%S')
    d2 = datetime.datetime.strptime(r, '%Y%m%d%H%M%S')
    delta = d1 - d2
    print d1, d2 ,delta.seconds

if __name__ == '__main__':
    l1 = '20171216170108'
    r1 = '20171216170225'
    dele_time(l1 ,r1)