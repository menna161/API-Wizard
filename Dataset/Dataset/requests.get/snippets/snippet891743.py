from __future__ import absolute_import, division, print_function, unicode_literals
import json
import logging
import os
import shutil
import tempfile
from functools import wraps
from hashlib import sha256
import sys
from io import open
import boto3
import requests
from botocore.exceptions import ClientError
from tqdm import tqdm
from urllib.parse import urlparse
from pathlib import Path
from urlparse import urlparse


def http_get(url, temp_file):
    req = requests.get(url, stream=True)
    content_length = req.headers.get('Content-Length')
    total = (int(content_length) if (content_length is not None) else None)
    progress = tqdm(unit='B', total=total)
    for chunk in req.iter_content(chunk_size=1024):
        if chunk:
            progress.update(len(chunk))
            temp_file.write(chunk)
    progress.close()
