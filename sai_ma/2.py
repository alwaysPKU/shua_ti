import sys
s = raw_input().strip()
dic = {}
for i in range(len(s)):
    if s[i] in dic.keys():
        continue
    else:
        dic[s[i]] = 1
ary = []
for i in dic.keys():
    ary.append(i)
ary.sort()
if '0' in ary:
    if len(ary) == 10:
        sys.stdout.write('10000000000')
    else:
        for i in range(len(ary)):
            if i != int(ary[i]):
                sys.stdout.write(str(i))
                break
else:
    if len(ary) < 9:
        for i in range(len(ary)):
            if i != ary[i]:
                sys.stdout.write(str(i+1))
                break
    elif len(ary) == 9:
        sys.stdout.write('10')
