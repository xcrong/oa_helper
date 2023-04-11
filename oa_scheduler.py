from oa_helper import oa_helper
import datetime
from time import sleep
from getConfig import startTime,endTime,interval

while True:
    now = datetime.datetime.now()
    if startTime <= now.hour <= endTime:
        oa_helper()
        sleep(interval * 60) 
    else:
        print(f"{now}.  Not work time....")
        sleep(interval * 10)