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


def get_from_cache(url, cache_dir=None):
    "\n    Given a URL, look for the corresponding dataset in the local cache.\n    If it's not there, download it. Then return the path to the cached file.\n    "
    if (cache_dir is None):
        cache_dir = PYTORCH_PRETRAINED_BERT_CACHE
    if ((sys.version_info[0] == 3) and isinstance(cache_dir, Path)):
        cache_dir = str(cache_dir)
    if (not os.path.exists(cache_dir)):
        os.makedirs(cache_dir)
    if url.startswith('s3://'):
        etag = s3_etag(url)
    else:
        response = requests.head(url, allow_redirects=True)
        if (response.status_code != 200):
            raise IOError('HEAD request failed for url {} with status code {}'.format(url, response.status_code))
        etag = response.headers.get('ETag')
    filename = url_to_filename(url, etag)
    cache_path = os.path.join(cache_dir, filename)
    if (not os.path.exists(cache_path)):
        with tempfile.NamedTemporaryFile() as temp_file:
            logger.info('%s not found in cache, downloading to %s', url, temp_file.name)
            if url.startswith('s3://'):
                s3_get(url, temp_file)
            else:
                http_get(url, temp_file)
            temp_file.flush()
            temp_file.seek(0)
            logger.info('copying %s to cache at %s', temp_file.name, cache_path)
            with open(cache_path, 'wb') as cache_file:
                shutil.copyfileobj(temp_file, cache_file)
            logger.info('creating metadata file for %s', cache_path)
            meta = {'url': url, 'etag': etag}
            meta_path = (cache_path + '.json')
            with open(meta_path, 'w', encoding='utf-8') as meta_file:
                json.dump(meta, meta_file)
            logger.info('removing temp file %s', temp_file.name)
    return cache_path
