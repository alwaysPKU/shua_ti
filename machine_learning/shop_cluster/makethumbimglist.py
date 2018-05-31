import os,sys,Image
def merge(imglist,output):
    picsize=150
    cur_width = 0
    cur_height= 20
    nth=0
    size=min(len(imglist),50)
    width = 1500
    nEachRow=width/picsize
    height = 20+min(picsize+(size-1)/nEachRow*picsize,750)
    row_num=(height-20)/picsize
    merge_img = Image.new('RGB', (width,height), 0xffffff)
    for img in imglist:
            nth += 1
            if not os.path.exists("imgs/"+img):
	            os.system("wget http://192.168.3.253:9333/"+img+" -P imgs/ >>log")
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


imgs=[]
cnt=0
last=""
ll=0
lines=open(sys.argv[1]).readlines()
lines.sort()
for line in lines:	
	array=line[:-1].split(" ")
	this=array[0]
	if last!=this and last!="":
		if len(imgs)>1:
#			if cnt==53:
#				print last,len(imgs),imgs,ll
			merge(imgs,str(cnt)+".jpg")
			cnt+=1
		
		imgs=[]
	last=this
	imgs.append(array[1])
	ll+=1
	if cnt==200:
		break


