import struct
f = open('./data_set/hq1.bin', 'rb')
w = open('./data_set/hq1_change.bin', 'ab')
count = f.read(8)
count2 = f.read(8)
w.write(count)
w.write(count2)
data, = struct.unpack('q', count)
data2, = struct.unpack('q', count2)
print data, data2
labels = range(int(data))
print labels[0]
for i in range(int(data)):
    line = f.read(8)
    w.write(line)
    line = f.read(8)
    # line_str = struct.unpack('qqf',line[:20])
    # print line_str
    label = struct.pack('q', labels[i])
    w.write(label)
    line = f.read(int(data2)*4)
    w.write(line)
    if i == 20:
        break
f.close()
