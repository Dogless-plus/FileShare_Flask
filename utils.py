import time
import datetime
import os
def beautify_time(timestamp):
    timeStruct = time.localtime(timestamp)
    return time.strftime('%Y-%m-%d %H:%M:%S',timeStruct)

def get_file_create_time(filePath):
    t = os.path.getctime(filePath)
    return beautify_time(t)
