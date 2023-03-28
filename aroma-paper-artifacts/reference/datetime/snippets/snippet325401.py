import sys
import urllib.request
import datetime
import requests
import re
import time
import types
import http.client
from pyquery import PyQuery as pq


@staticmethod
def strToTime(str, format='auto'):
    try:
        str_bak = str
        str = str.replace('年', '-').replace('月', '-').replace('日', '').replace('时', ':').replace('分', ':').replace('秒', '')
        if str.endswith(':'):
            str = str[0:(''.__len__() - 1)]
        if re.match('\\d{4}-\\d{1,2}-\\d{1,2} \\d{1,2}:\\d{1,2}:\\d{1,2}', str):
            format = '%Y-%m-%d %H:%M:%S'
        elif re.match('\\d{4}-\\d{1,2}-\\d{1,2} \\d{1,2}:\\d{1,2}', str):
            format = '%Y-%m-%d %H:%M'
        elif re.match('\\d{4}-\\d{1,2}-\\d{1,2}', str):
            format = '%Y-%m-%d'
        else:
            str = str_bak
            num = re.findall('^\\d*', str)[0]
            if (num != ''):
                num = int(num)
                time = datetime.datetime.now()
                str = str.replace('前', '').replace('分钟', '分').replace('小时', '时')
                if (str.rfind('秒') > (- 1)):
                    return (time + datetime.timedelta(seconds=(- num)))
                if (str.rfind('分') > (- 1)):
                    return (time + datetime.timedelta(minutes=(- num)))
                if (str.rfind('时') > (- 1)):
                    return (time + datetime.timedelta(hours=(- num)))
                if (str.rfind('天') > (- 1)):
                    return (time + datetime.timedelta(days=(- num)))
                if (str.rfind('周') > (- 1)):
                    return (time + datetime.timedelta(weeks=(- num)))
                if (str.rfind('月') > (- 1)):
                    return (time + datetime.timedelta(days=(- (num * 30))))
        date_time = datetime.datetime.strptime(str, format)
        return date_time
    except:
        return None
