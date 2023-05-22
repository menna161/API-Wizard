import fnmatch
import json
import logging
import os
import shutil
import sys
import tarfile
import tempfile
from contextlib import contextmanager
from functools import partial, wraps
from hashlib import sha256
from typing import Optional
from urllib.parse import urlparse
from zipfile import ZipFile, is_zipfile
import boto3
import requests
from botocore.config import Config
from botocore.exceptions import ClientError
from filelock import FileLock
from tqdm.auto import tqdm
from transformers import __version__
from torch.hub import _get_torch_home
from pathlib import Path
import torch
import tensorflow as tf


def get_from_cache(url, cache_dir=None, force_download=False, proxies=None, etag_timeout=10, resume_download=False, user_agent=None, local_files_only=False) -> Optional[str]:
    "\n    Given a URL, look for the corresponding file in the local cache.\n    If it's not there, download it. Then return the path to the cached file.\n\n    Return:\n        None in case of non-recoverable file (non-existent or inaccessible url + no cache on disk).\n        Local path (string) otherwise\n    "
    if (cache_dir is None):
        cache_dir = TRANSFORMERS_CACHE
    if isinstance(cache_dir, Path):
        cache_dir = str(cache_dir)
    os.makedirs(cache_dir, exist_ok=True)
    etag = None
    if (not local_files_only):
        if url.startswith('s3://'):
            etag = s3_etag(url, proxies=proxies)
        else:
            try:
                response = requests.head(url, allow_redirects=True, proxies=proxies, timeout=etag_timeout)
                if (response.status_code == 200):
                    etag = response.headers.get('ETag')
            except (EnvironmentError, requests.exceptions.Timeout):
                pass
    filename = url_to_filename(url, etag)
    cache_path = os.path.join(cache_dir, filename)
    if (etag is None):
        if os.path.exists(cache_path):
            return cache_path
        else:
            matching_files = [file for file in fnmatch.filter(os.listdir(cache_dir), (filename + '.*')) if ((not file.endswith('.json')) and (not file.endswith('.lock')))]
            if (len(matching_files) > 0):
                return os.path.join(cache_dir, matching_files[(- 1)])
            else:
                if local_files_only:
                    raise ValueError("Cannot find the requested files in the cached path and outgoing traffic has been disabled. To enable model look-ups and downloads online, set 'local_files_only' to False.")
                return None
    if (os.path.exists(cache_path) and (not force_download)):
        return cache_path
    lock_path = (cache_path + '.lock')
    with FileLock(lock_path):
        if resume_download:
            incomplete_path = (cache_path + '.incomplete')

            @contextmanager
            def _resumable_file_manager():
                with open(incomplete_path, 'a+b') as f:
                    (yield f)
            temp_file_manager = _resumable_file_manager
            if os.path.exists(incomplete_path):
                resume_size = os.stat(incomplete_path).st_size
            else:
                resume_size = 0
        else:
            temp_file_manager = partial(tempfile.NamedTemporaryFile, dir=cache_dir, delete=False)
            resume_size = 0
        with temp_file_manager() as temp_file:
            logger.info('%s not found in cache or force_download set to True, downloading to %s', url, temp_file.name)
            if url.startswith('s3://'):
                if resume_download:
                    logger.warn('Warning: resumable downloads are not implemented for "s3://" urls')
                s3_get(url, temp_file, proxies=proxies)
            else:
                http_get(url, temp_file, proxies=proxies, resume_size=resume_size, user_agent=user_agent)
        logger.info('storing %s in cache at %s', url, cache_path)
        os.rename(temp_file.name, cache_path)
        logger.info('creating metadata file for %s', cache_path)
        meta = {'url': url, 'etag': etag}
        meta_path = (cache_path + '.json')
        with open(meta_path, 'w') as meta_file:
            json.dump(meta, meta_file)
    return cache_path
