import os
import numpy as np

def Float(num):
    if num=='None':
        return 0
    return float(num)
def Float_abs(num):
    if num=='None':
        return 1000
    return abs(float(num))
def find_position(num):
    return round(num/1690486.*100,3)
fid_params={}
fids=[]
detects=[]
aligns=[]
angle1s=[]
blurs=[]
angle2s=[]
ages=[]
with open('result/shoptest_qualityall_lst') as f:
    line = f.readline()
    while line:
        ary = line.strip().split(' ')
        fid = ary[0]
        fids.append(fid)
        tmp = ary[1].split(',')
        detects.append(Float(tmp[0]))
        aligns.append(Float(tmp[1]))
        angle1s.append(Float_abs(tmp[-3]))
        blurs.append(Float(tmp[-2]))
        angle2s.append(Float_abs(tmp[-1]))
        fid_params[fid]=ary[1]
        line = f.readline()

fid_age={}
with open('result/shoptest_parametersall_lst') as f:
    line = f.readline()
    while line:
        ary = line.strip().split(' ')
        fid = ary[0]
        tmp = ary[1].split(',')
        need_save=float(tmp[-4])
        fid_age[fid]=need_save
        line = f.readline()
    for fid in fids:
        if fid_age.has_key(fid):
            ages.append(Float(fid_age[fid]))
        else:
            ages.append(0)

#print map(len, [fids,detects,aligns,angle1s,blurs,angle2s,ages])

detc_sort=np.argsort(np.argsort(np.array(detects)))
detects_pos=map(find_position, detc_sort)
#print detects_pos
ali_sort=np.argsort(np.argsort(np.array(aligns)))
aligns_pos=map(find_position, ali_sort)

ang1_sort=np.argsort(np.argsort(-np.array(angle1s)))
angle1s_pos=map(find_position, ang1_sort)

blur_sort=np.argsort(np.argsort(np.array(blurs)))
blur_pos=map(find_position, blur_sort)

ang2_sort=np.argsort(np.argsort(-np.array(angle2s)))
angle2s_pos=map(find_position, ang2_sort)


age_sort=np.argsort(np.argsort(np.array(ages)))
ages_pos=map(find_position, age_sort)

with open('shaop_params_new','w') as w: 
    for fid,age,detct_pos,align_pos,ang1_pos,blur_pos,ang2_pos,age_pos in zip(fids,ages,detects_pos,aligns_pos,angle1s_pos,blur_pos,angle2s_pos,ages_pos):
        params =fid+' '+fid_params[fid]+','+str(int(age))+','+str(detct_pos)+'%,'+str(align_pos)+'%,'+str(ang1_pos)+'%,'+str(blur_pos)+'%,'+str(ang2_pos)+'%,'+str(age_pos)+'%\n'
        w.write(params)


