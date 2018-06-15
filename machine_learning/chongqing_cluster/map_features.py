from __future__ import print_function
import os,re
from multiprocessing import Pool


w1=open('chongqing_001-011_featlst','aw')
condition1=('001','002','003','004','005','006','007','008','009','010','011')
w2=open('chongqing_012-019_featlst','aw')
condition2=('012','013','014','015','016','017','018','019')
w3=open('chongqing_020-043_featlst','aw')
condition3=('020','021','022','023','024','025','026','027','028','029','030','031','032','033','034','035','036','037','038','039','040','041','042','043')
w4=open('chongqing_044-054_featlst','aw')
condition4=('044','045','046','047','048','049','050','051','052','053','054')
w5=open('chongqing_401_featlst','aw')
condition5=('401')
w6=open('chongqing_402_featlst','aw')
condition6=('402')
w7=open('chongqing_403_featlst','aw')
condition7=('403')
w8=open('chongqing_501_featlst','aw')
condition8=('501')
w9=open('chongqing_502-504_featlst','aw')
condition9=('502','503','504')
w10=open('chongqing_506-507_featlst','aw')
condition10=('506','507')
w11=open('chongqing_800_featlst','aw')
condition11=('800')
w12=open('chongqing_900_featlst','aw')
condition12=('900')

def judege(file_path):
    with open(file_path) as f:
        line = f.readline()
        while line:
            fid=line.split('/',3)[2]
            if fid in condition1:
                w1.write(line)
            elif fid in condition2:
                w2.write(line)
            elif fid in condition3:
                w3.write(line)
            elif fid in condition4:
                w4.write(line)
            elif fid in condition5:
                w5.write(line)
            elif fid in condition6:
                w6.write(line)
            elif fid in condition7:
                w7.write(line)
            elif fid in condition8:
                w8.write(line)
            elif fid in condition9:
                w9.write(line)
            elif fid in condition10:
                w10.write(line)
            elif fid in condition11:
                w11.write(line)
            elif fid in condition12:
                w12.write(line)
            else:
                print ('wrong:',fid)
            line = f.readline()

def sayHi(fi):
    return fi

if __name__ == '__main__':
    command='ls ../cqdata/features/mergecq*'
    files=os.popen(command).read().splitlines()
    print ('nums of file:',len(files))
    print (files)
    p = Pool(20)
    for i, file_path in enumerate(files):
        print ('process:%2d,file:%s'%(i,file_path))
   #     judege(file_path)
        p.apply_async(sayHi, args=(file_path,), callback=judege)
    p.close()
    p.join()
    
    for i in [w1,w2,w3,w4,w5,w6,w7,w8,w9,w10,w11,w12]:
        i.close()
