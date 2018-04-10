import sys


def panding_huiwen(s):
    if s == '' or None:
        return False
    else:
        length = len(s)
        for i in range(length/2):
            if s[i] == s[length-1-i]:
                continue
            else:
                return False
        return True

# s = sys.stdin.readline()
s = '12345678'

print s[0:-1:2]
