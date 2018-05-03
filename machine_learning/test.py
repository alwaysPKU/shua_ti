with open('./data_set/data.csv') as f:
    num = 0
    line = f.readline()
    while line:
        print line
        num += 1
        if num == 5:
            break
        line = f.readline()