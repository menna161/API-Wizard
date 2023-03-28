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


def generate_item(query, pid):
    (item, _, state) = parse(query)
    n = datetime.datetime.utcnow()
    item['modifiedTime'] = (n.strftime('%Y-%m-%dT%H:%M:%S.%f')[:(- 3)] + '+0000')
    item['id'] = object_id()
    item['status'] = 0
    item['timeZone'] = 'CST'
    item['content'] = ''
    item['sortOrder'] = 0
    item['items'] = []
    item['progress'] = 0
    if (state == S_NONE):
        item['isAllDay'] = None
    else:
        item['isAllDay'] = ((state & S_TIME) == 0)
    item['projectId'] = pid
    return item
