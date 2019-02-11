import pymysql
import datetime
import json
import time
from flask import request


def ftime(a):
    if a.days == 0:
        if a.seconds // 3600 == 0:
            seconds = (a.seconds % 3600) // 60
            if seconds != 0:
                return f"{seconds} 分钟前"
            else:
                return "刚刚"
        else:
            return f"{a.seconds // 3600} 小时前"
    else:
        return f"{a.days} 天前"

def check_login_status():
        username = request.cookies.get('username')
        if username == None:
            return "0"  #未登录
        else:
            return username










    




        



