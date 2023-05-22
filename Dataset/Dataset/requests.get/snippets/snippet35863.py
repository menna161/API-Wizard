import argparse
import logging
import requests
import retrying
import subprocess
import sys


@retrying.retry(wait_fixed=WAIT, stop_max_delay=MAX_DELAY)
def check_homepage(host, port):
    'Check homepage health by requesting via HTTP.'
    logger.info('Checking homepage...')
    r = requests.get(('http://%s:%d' % (host, port)))
    if (r.status_code >= 400):
        logger.error('[%d] %s', r.status_code, r.text)
    assert (r.status_code < 400)
