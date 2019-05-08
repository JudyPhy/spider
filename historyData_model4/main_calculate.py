# coding=gbk
from dragon import dragon
import datetime

start_time = datetime.datetime.now()

dragon.main()

delta_time = datetime.datetime.now() - start_time
print('cost time:', delta_time)
