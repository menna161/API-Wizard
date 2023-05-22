import argparse
import json
import os
import sys
import lxml.html as html
import requests


def get_session():
    'requests.Session: Get requests session.'
    session = requests.Session()
    session.headers = {'Host': 'www.pinterest.com', 'Referer': 'https://www.pinterest.com/', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.113 Safari/537.36 Vivaldi/2.1.1337.51', 'X-APP-VERSION': 'ab1af2a', 'X-B3-SpanId': '183fc9cb02974b', 'X-B3-TraceId': '14f603d2caa27c', 'X-Pinterest-AppState': 'active', 'X-Requested-With': 'XMLHttpRequest'}
    return session
