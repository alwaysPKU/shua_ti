import datetime
l_time = '20171122121211123456'
r_time = '20171122121211123456'
d1 = datetime.datetime.strptime(l_time, '%Y%m%d%H%M%S%f')
d2 = datetime.datetime.strptime(r_time, '%Y%m%d%H%M%S%f')
print abs(d1-d2).total_seconds()==0