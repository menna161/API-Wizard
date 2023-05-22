import os
import re
import json
from datetime import datetime
import numpy as np
import requests
from arxivtimes_indicator.data_api import DataApi


def aggregate_per_month(self, user_id='', month=6, use_genre=True):
    posts = self.get_recent(user_id)
    stat = {}
    get_ym = (lambda date_str: date_str.split('T')[0].rsplit('-', 1)[0].replace('-', '/'))
    for p in posts:
        ym = get_ym(p['created_at'])
        kinds = (p['genres'] if use_genre else p['labels'])
        if (ym not in stat):
            stat[ym] = {}
        for k in kinds:
            if (k not in stat[ym]):
                stat[ym][k] = 0
            stat[ym][k] += 1
    genres = list(set(self.LABEL_TO_GENRE.values()))
    labels = list(self.LABEL_TO_GENRE.keys())
    kinds = (genres if use_genre else labels)
    (_year, _month) = (datetime.now().year, datetime.now().month)
    yms = []
    for i in range(month):
        yms.append('{}/{}'.format(_year, str(_month).zfill(2)))
        _month = (_month - 1)
        if (_month <= 0):
            _month = (_month + 12)
            _year = (_year - 1)
    for ym in yms:
        if (ym not in stat):
            stat[ym] = {}
        for k in kinds:
            if (k not in stat[ym]):
                stat[ym][k] = 0
    return stat
