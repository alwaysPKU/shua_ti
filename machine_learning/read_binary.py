import struct


if __name__ == '__main__':
    f = open('./data_set/hq1_change.bin', 'rb')
    count = f.read(8)
    count2= f.read(8)
    data, = struct.unpack('q', count)
    data2, = struct.unpack('q', count2)
    print data, data2
    for i in range(int(data)):
        print 'line', i
        count3 = f.read(8)
        count4 = f.read(8)
        label, =  struct.unpack('q', count3)
        flag, = struct.unpack('q', count4)
        features = []
        for j in range(int(data2)):
            count5 = f.read(4)
            tmp, = struct.unpack('f', count5)
            features.append(tmp)
        print label, flag, features
        if i == 20:
            break
    f.close()
