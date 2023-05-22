from __future__ import absolute_import, division, print_function, unicode_literals
import sys
import json
import logging
import os
import six
import shutil
import tempfile
import fnmatch
from functools import wraps
from hashlib import sha256
from io import open
import boto3
from botocore.config import Config
from botocore.exceptions import ClientError
import requests
from tqdm import tqdm
from torch.hub import _get_torch_home
from urllib.parse import urlparse
from pathlib import Path
from urlparse import urlparse


def http_get(url, temp_file, proxies=None):
    req = requests.get(url, stream=True, proxies=proxies)
    content_length = req.headers.get('Content-Length')
    total = (int(content_length) if (content_length is not None) else None)
    progress = tqdm(unit='B', total=total)
    for chunk in req.iter_content(chunk_size=1024):
        if chunk:
            progress.update(len(chunk))
            temp_file.write(chunk)
    progress.close()
