def merge_labels(labels_fix):
    '''
    :param labels_fix:[[],[],[],[]] 
    :return: [[],[]]
    '''
    map_1 = {}
    map_2 = {}
    for i, tumple in enumerate(labels_fix):
        if not map_1.has_key(tumple[0]) and not map_1.has_key(tumple[1]):
            map_1[tumple[0]] = i
            map_1[tumple[1]] = i
            map_2[i] = [tumple[0], tumple[1]]
        elif not map_1.has_key(tumple[0]):
            map_1[tumple[0]] = map_1[tumple[1]]
            map_2[map_1[tumple[1]]].append(tumple[0])
        elif not map_1.has_key(tumple[1]):
            map_1[tumple[1]] = map_1[tumple[0]]
            map_2[map_1[tumple[0]]].append(tumple[1])
        else:
            if map_1[tumple[0]] != map_1[tumple[1]]:
                if len(map_2[map_1[tumple[0]]]) >= len(map_2[map_1[tumple[1]]]):
                    map_2[map_1[tumple[0]]] = map_2[map_1[tumple[0]]] + map_2[map_1[tumple[1]]]
                    tmp = map_1[tumple[1]]
                    for i in map_2[map_1[tumple[1]]]:
                        map_1[i] = map_1[tumple[0]]
                    del map_2[tmp]
                else:
                    map_2[map_1[tumple[1]]] = map_2[map_1[tumple[1]]] + map_2[map_1[tumple[0]]]
                    tmp = map_1[tumple[0]]
                    for i in map_2[map_1[tumple[0]]]:
                        map_1[i] = map_1[tumple[1]]
                    del map_2[tmp]
            else:
                continue
                # for key, values in map_2.items():
                #     print key, values
                # print '================='
    return [i for i in map_2.values()]

if __name__ == '__main__':
    a = [[1,2], [1,3], [2, 3], [2, 1], [5, 6], [6, 5], [1, 2], [7, 8], [11, 12], [5, 7],[11,3],
         [8, 3]]
    print merge_labels(a)