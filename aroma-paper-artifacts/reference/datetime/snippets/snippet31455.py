import json
import datetime
import time
import os.path
import random
import re
import sys
import os
import urllib.request
import urllib.error
import traceback


def parse(query):
    q = {'title': None, 'priority': 0, 'dueDate': None, 'startDate': None, 'reminder': '', 'reminders': []}
    q['title'] = query
    m = re.search('(!+)', q['title'])
    if m:
        q['priority'] = ((2 * len(m.group(1))) - 1)
        q['title'] = re.sub('!+', '', q['title'])
    q['title'] = q['title'].strip()
    state = S_NONE
    d = datetime.datetime.now()
    d = d.replace(hour=0, minute=0, second=0, microsecond=0)
    t = None
    while True:
        t = token(q, t)
        if (not t):
            break
        if (state == S_NONE):
            m = re.match('(\\d{1,2}):(\\d{1,2})', t)
            if m:
                d = d.replace(hour=int(m.group(1)), minute=int(m.group(2)))
                if (d < datetime.datetime.now()):
                    d += datetime.timedelta(days=1)
                state = S_TIME
                continue
        if (state <= S_TIME):
            if (t in ('tomorrow', 'tmr')):
                state |= S_DAY
                if (d.date() == datetime.date.today()):
                    d += datetime.timedelta(days=1)
                break
            m = re.match('(\\d{1,2})-(\\d{1,2})', t)
            if m:
                state |= S_DAY
                d = d.replace(month=int(m.group(1)), day=int(m.group(2)))
                if (d < datetime.datetime.now()):
                    d = d.replace(year=(d.year + 1))
                continue
            m = re.match('\\b({0})\\b'.format('|'.join(WEEKDAY.keys())), t, re.I)
            if m:
                state |= S_WEEKDAY
                n = WEEKDAY[m.group(1)]
                d += datetime.timedelta(days=1)
                while (d.weekday() != n):
                    d += datetime.timedelta(days=1)
                continue
        if ((t == 'next') and ((state & S_WEEKDAY) != 0)):
            if (datetime.datetime.now().weekday() < d.weekday()):
                d += datetime.timedelta(days=7)
            break
        if (t == 'every'):
            if (state == S_TIME):
                q['repeatFlag'] = 'RRULE:FREQ=DAILY;INTERVAL=1'
            elif ((state & S_DAY) != 0):
                q['repeatFlag'] = 'RRULE:FREQ=MONTHLY;INTERVAL=1'
            elif ((state & S_WEEKDAY) != 0):
                q['repeatFlag'] = 'RRULE:FREQ=WEEKLY;INTERVAL=1'
            break
        t = None
        break
    token(q, t)
    if (state != S_NONE):
        u = d.astimezone(UTC())
        q['startDate'] = q['dueDate'] = '{0}{1:%z}'.format(u.strftime('%Y-%m-%dT%H:%M:%S.%f')[:(- 3)], u)
        if ((state & S_TIME) != 0):
            q['reminder'] = DEFAULT_TRIGGER
            q['reminders'].append({'id': object_id(), 'trigger': DEFAULT_TRIGGER})
    return (q, d, state)
