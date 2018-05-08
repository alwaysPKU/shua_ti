import json as js


dic = dict()
dic['features_file'] = 'zhangwei_featlst_rdele_labels_0.7'
dic['labels_file_2'] = 'labels_0.6_0.68_0.7_1.0s'
dic['labels_file_1'] = 'labels_0.68_dele_0.7'
dic['parameters_file'] = 'zhangwei_parameters'
dic['out_put'] = dic['labels_file_2'].split('s_')[1]

# js.dump(dic)
with open('datavisual_params', 'w') as w:
    w.write(js.dumps(dic))

with open('datavisual_params') as f:
    line = f.readline()
    duixiang = js.loads(line)
print line

