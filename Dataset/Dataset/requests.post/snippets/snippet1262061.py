import configparser
import getpass
import hashlib
import logging
import os
from pathlib import Path
import requests
import sys
from urllib.parse import urlparse
from .common import Metadata
from . import build
import keyring


def verify(metadata: Metadata, repo_name):
    'Verify the metadata with the PyPI server.\n    '
    repo = get_repository(repo_name)
    data = build_post_data('verify', metadata)
    resp = requests.post(repo['url'], data=data, auth=(repo['username'], repo['password']))
    resp.raise_for_status()
    log.info('Verification succeeded')
