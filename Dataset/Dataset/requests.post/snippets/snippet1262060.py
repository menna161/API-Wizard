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


def upload_file(file: Path, metadata: Metadata, repo):
    'Upload a file to an index server, given the index server details.\n    '
    data = build_post_data('file_upload', metadata)
    data['protocol_version'] = '1'
    if (file.suffix == '.whl'):
        data['filetype'] = 'bdist_wheel'
        py2_support = (not (metadata.requires_python or '').startswith(('3', '>3', '>=3')))
        data['pyversion'] = (('py2.' if py2_support else '') + 'py3')
    else:
        data['filetype'] = 'sdist'
    with file.open('rb') as f:
        content = f.read()
        files = {'content': (file.name, content)}
        data['md5_digest'] = hashlib.md5(content).hexdigest()
    log.info('Uploading %s...', file)
    resp = requests.post(repo['url'], data=data, files=files, auth=(repo['username'], repo['password']))
    resp.raise_for_status()
