import sys,os
import Image

def merge(imglist,output):
    picsize=150
    cur_width = 0
    cur_height= 20
    nth=0
   # size=min(len(imglist),100)
    size=min(len(imglist),300)
   # width = 1500
    width = 3000
    nEachRow=width/picsize
   # height = 20+min(picsize+(size-1)/nEachRow*picsize,750)
    height = 20+min(picsize+(size-1)/nEachRow*picsize,2250)
    row_num=(height-20)/picsize
    merge_img = Image.new('RGB', (width,height), 0xffffff)
    step = len(imglist)/300 + 1
    for i in range(0, len(imglist),step):
        img = imglist[i]
        nth += 1
        if not os.path.exists("imgs/"+img):
                os.system("wget http://192.168.3.253:9333/"+img+" -P imgs/ >/dev/null 2>&1")
        fp = open("imgs/"+img,'r')
        img = Image.open(fp)
        if img.mode != 'RGB':
            img = img.convert('RGB')
        merge_img.paste(img.resize((picsize,picsize),Image.BICUBIC), (cur_width, cur_height))
        cur_width += picsize
        if nth%nEachRow==0:
            cur_height+=picsize
            cur_width=0
        if nth==nEachRow*row_num:
            break
    merge_img.save(output,quality=100)

if __name__ == '__main__':
    name_labels_file = sys.argv[1]
    labels_align = sys.argv[2]
    name = sys.argv[3]
    # find label
    label = os.popen("grep " + name + ' ' + name_labels_file).read().split(' ')[1]
    lines = os.popen("cat " + labels_align).read().splitlines()
    lines.sort()
    res = []
    mark = False
    for i in lines:
        rmp_ary = i.split(' ')
        if int(rmp_ary[0]) == label:
            res.append(rmp_ary[1])
            mark = True
        else:
            if mark:
                break
            else:
                continue
    merge(res, name+label+'.jpg')
