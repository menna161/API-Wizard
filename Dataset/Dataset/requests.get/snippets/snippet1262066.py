import logging
import os
from pathlib import Path
import re
import requests
import sys
from .common import InvalidVersion


def _download_classifiers():
    'Get the list of valid trove classifiers from PyPI'
    log.info('Fetching list of valid trove classifiers')
    resp = requests.get('https://pypi.org/pypi?%3Aaction=list_classifiers')
    resp.raise_for_status()
    cache_dir = get_cache_dir()
    try:
        cache_dir.mkdir(parents=True)
    except FileExistsError:
        pass
    with (get_cache_dir() / 'classifiers.lst').open('wb') as f:
        f.write(resp.content)
