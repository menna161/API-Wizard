import sys
import archon.exchange.exchanges as exc
import archon.facade as facade
import archon.broker as broker
import archon.plugins.mail as mail
import json
import requests
from jinja2 import Template
import jinja2
import pickle
from datetime import datetime


def write_to_file(html):
    date_broker_format = '%Y-%m-%d'
    from datetime import datetime
    ds = datetime.now().strftime('%Y%m%d')
    fn = (('../../balance_report' + ds) + '.html')
    with open(fn, 'w') as f:
        f.write(html)
