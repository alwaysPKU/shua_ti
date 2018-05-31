def Float(num):
    if num=='None':
        return 0
    return float(num)
def Float_abs(num):
    if num=='None':
        return 1000
    return abs(float(num))

detect_thr=0.6
align_thr=0.83
blur_thr=0.15
angle_thr=40

#fids=[]
out_put = 'new_feature_'+str(detect_thr)+'_'+str(align_thr)+'_'+str(angle_thr)+'_'+str(blur_thr)
w = open(out_put,'w')
f1 = open('result/shoptest_featuresall_lst')
count=0
with open('shaop_params_new') as f:
    line = f.readline()
    line1 = f1.readline()
    while line and line1:
        ary=line.strip().split(' ')[1].split(',')
        detect=Float(ary[0])
        align=Float(ary[1])
        angle1 = Float_abs(ary[3])
        blur = Float(ary[4])
        angle2 = Float_abs(ary[5])
        if detect>detect_thr and align > align_thr and angle1 < angle_thr and blur > blur_thr and angle2 < angle_thr:
            w.write(line1)
        else:
           count+=1
           print line1
        line = f.readline()
        line1 = f1.readline()
print count

f1.close()
w.close()
