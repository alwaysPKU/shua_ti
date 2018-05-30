
def yu(a):
    if a&1:
        print a, '&1 is true'
    if a&2:
        print a, '&2 is true'
    if a&4:
        print a, '&4 is true'

if __name__ == '__main__':
    for a in [1,2,4,7]:
        yu(a)
