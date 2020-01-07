from database.user import UserDB
from database.journal import JournalDB
from database.record import RecordDB
import datetime
import time

# 字符类型的时间
tss1 = '2019-12-29 23:40:00'
tss2 = '2020-1-7 23:40:00'
# 转为时间数组
timeArray1 = time.strptime(tss1, "%Y-%m-%d %H:%M:%S")
timeArray2 = time.strptime(tss2, "%Y-%m-%d %H:%M:%S")

d1 = datetime.datetime(timeArray1.tm_year, timeArray1.tm_mon, timeArray1.tm_mday)
d2 = datetime.datetime(timeArray2.tm_year, timeArray2.tm_mon, timeArray2.tm_mday)

print((d2 - d1).days)
# print (timeArray)
# timeArray可以调用tm_year等
# print (timeArray.tm_year)   # 2013
# 转为时间戳
# timeStamp = int(time.mktime(timeArray))
# print (timeStamp)  # 1381419600
