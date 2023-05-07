from concurrent import futures
from http.client import HTTPSConnection
import logging
import time
from random import randint
import click
from click._termui_impl import ProgressBar
from ._urls import URLS, expand_url_tree, ExpandedURL


def check_url(expanded: ExpandedURL, progress_bar: ProgressBar):
    (host, rest) = split(expanded.url)
    time.sleep(randint(1, 4))
    progress_bar.update(1)
    conn = HTTPSConnection(host)
    conn.request('HEAD', rest)
    response = conn.getresponse()
    if (response.status == 200):
        logger.debug('SUCCESS: URL check for {} {} MongoDB {}'.format(expanded.os_name, expanded.os_version, expanded.version))
    else:
        logger.error('FAIL: URL check for {} {} MongoDB {}, {}, reason: {} {}'.format(expanded.os_name, expanded.os_version, expanded.version, expanded.url, response.status, response.reason))
        return expanded
