# coding=utf-8

import re
import string
from log_helper import LogHelper
import time


class DateTimeHelper:
    
    def __init__(self):
        LogHelper.log("created")
    
    @staticmethod
    def getDateString():
        localtime = time.localtime()
        timeString = time.strftime("%Y-%m-%d", localtime)
        return timeString
    
    @staticmethod
    def getDateTimeString():
        localtime = time.localtime()
        timeString = time.strftime("%Y-%m-%d %H:%M:%S", localtime)
        return timeString
    
if __name__=="__main__":
    print("main")
    print("date string=" + DateTimeHelper.getDateString())
    print("datetime string=" + DateTimeHelper.getDateTimeString())
    print("exit")
    
    