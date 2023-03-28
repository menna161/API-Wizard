import datetime
import hashlib
import json
import random
import socket
import time
import os
import decimal
from copy import deepcopy
from dateutil.relativedelta import relativedelta
from requests.cookies import RequestsCookieJar
from atp.utils.common import read_custom


def generate_idcard(age=None):
    '\n生成身份证号，生成规则同真实身份证，18位，最后一位可以是数字或者X\n    :return:身份证号\n    '
    ARR = (7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2)
    LAST = ('1', '0', 'X', '9', '8', '7', '6', '5', '4', '3', '2')
    u' 随机生成新的18为身份证号码 '
    t = time.localtime()[0]
    first_list = ['362402', '362421', '362422', '362423', '362424', '362425', '362426', '362427', '362428', '362429', '362430', '362432', '110100', '110101', '110102', '110103', '110104', '110105', '110106', '110107', '110108', '110109', '110111', '320101', '320102', '320103', '320104', '320105', '320106']
    try:
        age = int(age)
        if ((0 > age) or (age > 200)):
            target_year = random.randint((t - 50), (t - 19))
        else:
            target_year = (datetime.datetime.now().year - age)
    except (ValueError, TypeError):
        target_year = random.randint((t - 50), (t - 19))
    x = ('%06d%04d%02d%02d%03d' % (int(random.choice(first_list)), target_year, random.randint(1, 12), random.randint(1, 28), random.randint(1, 999)))
    y = 0
    for i in range(17):
        y += (int(x[i]) * ARR[i])
    id_card = ('%s%s' % (x, LAST[(y % 11)]))
    return id_card
