import sys, os
import datetime

def get_id_time(fid):
    id, time = '', ''
    key = fid.split('/')[-1].rstrip('.jpg')
    ary = key.split('_')
    if len(ary) == 6:
        id_time = ary[0] + ary[1] + ary[2]
    else:
        id_time = ary[0] + ary[1]
    return id_time


if __name__ == '__main__':
    num = 0
    t1 = datetime.datetime.now()
    tmp_dict = {}
    tmp_set = set()
    dele_list = []
    file_path = sys.argv[1]
    img_list = os.popen("awk '{print$1}' " + file_path).read().splitlines()
    for index, img_name in enumerate(img_list):
        id_name = get_id_time(img_name)
        if tmp_dict.has_key(id_name):
            print tmp_dict[id_name]
            tmp_set.add(id_name)
            tmp_dict[id_name].append(index)
            num+=1
            print id_name, '==add value', tmp_dict[id_name]
        else:
            tmp_dict[id_name]=[index]
    for i in tmp_set:
        value = tmp_dict[i]
        num = len(value)
        for j in range(num):
            for k in range(num):
                if k == j:
                    continue
                else:
                    dele_list.append([value[j], value[k]])
    t2 = datetime.datetime.now()
    print 'end compute_dele:', t2-t1
    # print dele_list



