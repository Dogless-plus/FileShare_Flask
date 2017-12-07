import time
from hashlib import md5
import os
from os import path
def beautify_time(timestamp):
    timeStruct = time.localtime(timestamp)
    return time.strftime('%Y-%m-%d %H:%M:%S',timeStruct)

def get_file_create_time(filePath):
    t = os.path.getctime(filePath)
    return beautify_time(t)

def get_md5(code):
    return md5(str(code).encode("utf-8")).hexdigest()

def sizeof_fmt(num, suffix='B'):
    for unit in [' ', ' K', ' M', ' G', ' T', ' P', ' E', ' Z']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)

def get_filesize(filename):
    return sizeof_fmt(path.getsize(filename))