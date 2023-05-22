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


def get_from_cache(url, cache_dir=None, force_download=False, proxies=None):
    "\n    Given a URL, look for the corresponding dataset in the local cache.\n    If it's not there, download it. Then return the path to the cached file.\n    "
    if (cache_dir is None):
        cache_dir = PYTORCH_TRANSFORMERS_CACHE
    if ((sys.version_info[0] == 3) and isinstance(cache_dir, Path)):
        cache_dir = str(cache_dir)
    if ((sys.version_info[0] == 2) and (not isinstance(cache_dir, str))):
        cache_dir = str(cache_dir)
    if (not os.path.exists(cache_dir)):
        os.makedirs(cache_dir)
    if url.startswith('s3://'):
        etag = s3_etag(url, proxies=proxies)
    else:
        try:
            response = requests.head(url, allow_redirects=True, proxies=proxies)
            if (response.status_code != 200):
                etag = None
            else:
                etag = response.headers.get('ETag')
        except EnvironmentError:
            etag = None
    if ((sys.version_info[0] == 2) and (etag is not None)):
        etag = etag.decode('utf-8')
    filename = url_to_filename(url, etag)
    cache_path = os.path.join(cache_dir, filename)
    if ((not os.path.exists(cache_path)) and (etag is None)):
        matching_files = fnmatch.filter(os.listdir(cache_dir), (filename + '.*'))
        matching_files = list(filter((lambda s: (not s.endswith('.json'))), matching_files))
        if matching_files:
            cache_path = os.path.join(cache_dir, matching_files[(- 1)])
    if ((not os.path.exists(cache_path)) or force_download):
        with tempfile.NamedTemporaryFile() as temp_file:
            logger.info('%s not found in cache or force_download set to True, downloading to %s', url, temp_file.name)
            if url.startswith('s3://'):
                s3_get(url, temp_file, proxies=proxies)
            else:
                http_get(url, temp_file, proxies=proxies)
            temp_file.flush()
            temp_file.seek(0)
            logger.info('copying %s to cache at %s', temp_file.name, cache_path)
            with open(cache_path, 'wb') as cache_file:
                shutil.copyfileobj(temp_file, cache_file)
            logger.info('creating metadata file for %s', cache_path)
            meta = {'url': url, 'etag': etag}
            meta_path = (cache_path + '.json')
            with open(meta_path, 'w') as meta_file:
                output_string = json.dumps(meta)
                if ((sys.version_info[0] == 2) and isinstance(output_string, str)):
                    output_string = unicode(output_string, 'utf-8')
                meta_file.write(output_string)
            logger.info('removing temp file %s', temp_file.name)
    return cache_path
