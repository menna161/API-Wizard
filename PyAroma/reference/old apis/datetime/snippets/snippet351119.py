import os
import sys
from collections import Counter, defaultdict
from datetime import datetime
import dateutil.parser
import dateutil.relativedelta
from arxivtimes_indicator.data_api import DataApi
from peewee import *
from playhouse.db_url import connect
from playhouse.shortcuts import model_to_dict


def aggregate_per_month(self, user_id='', month=5, use_genre=True):
    now = datetime.now()
    start_time = (now - dateutil.relativedelta.relativedelta(months=month))
    start_time_str = start_time.strftime('%Y-%m-01 00:00:00+00:00')
    if user_id:
        issues = Issue.select().where((Issue.user_id == user_id)).where((Issue.created_at >= start_time_str))
    else:
        issues = Issue.select().where((Issue.created_at >= start_time_str))
    stat = defaultdict(Counter)
    for issue in issues:
        if isinstance(issue.created_at, datetime):
            key = issue.created_at.strftime('%Y/%m')
        else:
            key = dateutil.parser.parse(issue.created_at).strftime('%Y/%m')
        issue_d = self.issue_to_dict(issue)
        kinds = (issue_d['genres'] if use_genre else issue_d['labels'])
        for k in kinds:
            stat[key][k] += 1
    genres = list(set(self.LABEL_TO_GENRE.values()))
    labels = list(self.LABEL_TO_GENRE.keys())
    kinds = (genres if use_genre else labels)
    (_year, _month) = (start_time.year, start_time.month)
    yms = []
    for i in range(month):
        ym = '{}/{}'.format(_year, str(_month).zfill(2))
        if (ym not in stat):
            stat[ym] = {}
        for k in kinds:
            if (k not in stat[ym]):
                stat[ym][k] = 0
        stat[ym] = dict(stat[ym])
        _month = (_month + 1)
        if (_month > 12):
            _month = (_month - 12)
            _year = (_year + 1)
    return stat
