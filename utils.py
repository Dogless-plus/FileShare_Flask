import time
from hashlib import md5
import os
from os import path,listdir,sep
import pandas as pd
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

def get_foldersize(foldername):
    size = sum(path.getsize(sep.join([path.abspath(foldername),f])) for f in listdir(foldername))
    return sizeof_fmt(size)

def sort_by_time(codes,files,filesizes,times):
    df = pd.DataFrame(list(zip(codes,files,filesizes,times)),columns=["codes","files","filesizes","times"])
    df = df.sort_values("times",axis=0,ascending=False)
    codes, files, filesizes, times = list(df["codes"]),list(df["files"]),list(df["filesizes"]),list(df["times"])
    return codes,files,filesizes,times
