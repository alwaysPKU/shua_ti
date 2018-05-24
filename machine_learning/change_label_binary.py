import struct
import datetime
import sys


def time():
    return datetime.datetime.now()


if __name__ == '__main__':
    file_labels = sys.argv[1]
    file_jidi = sys.argv[2]
    out_put = 'chongqing_labels_0.5_0.7_1.0s_new'
    print 'imput :', file_labels, file_jidi
    print 'out_put:', out_put
    # count fid_labels_num
    t1 = time()
    # fid = []
    labels = []
    label_num = {}
    num = 0
    with open(file_labels) as f_labels:
        lines = f_labels.readlines()
        # lines.sort(key=lambda x:x.strip().split(' '))
        for line in lines:
            line = line.strip().split(' ')
            # fid.append(line[0])
            labels.append(line[1])
            if label_num.has_key(line[1]):
                label_num[line[1]] += 1
            else:
                label_num[line[1]] = 1
    t2 = time()
    print 'num of labels:', len(label_num)
    print 'end read labels:', t2, t2-t1
    new_label = 0
    bad_cluster='1108951'
   # for label in labels:
   #     if label_num[label]!=-1:
   #         if label_num[label] <10 or label==bad_cluster:
   #             label_num[label] = -1
   #         else:
   #             num += 1
    for k, v in label_num.items():
        if v < 10 or k == bad_cluster:
            label_num[k]=-1
        else:
            label_num[k] = new_label
            new_label += 1
            num+=v
    t3 = time()
    print 'you xiao shuju liang:', num
    print 'num of cluster:', new_label+1
    print 'big bad cluster', bad_cluster
    print 'end change label:', t3, t3-t2
    # change jidi label
    f = open(file_jidi, 'rb')
    w = open(out_put, 'ab')
    count = f.read(8)
    count2 = f.read(8)
    count_new = struct.pack('q', num)
    w.write(count_new)
    w.write(count2)
    data, = struct.unpack('q', count)
    data2, = struct.unpack('q', count2)
    print data, data2
    # labels = range(int(data))
    for i in range(int(data)):
        label = labels[i]
        if label_num[label]!=-1:
            line = f.read(16+int(data2)*4)
            label = struct.pack('q', label_num[label])
            line = label+line[8:]
            w.write(line)
        else:
            line = f.read(16 + int(data2) * 4)
            continue
        if i%10000 == 0:
            print i
    f.close()
    w.close()
    t4 = time()
    print 'end write and change jidi labels:', t4, t4-t3

