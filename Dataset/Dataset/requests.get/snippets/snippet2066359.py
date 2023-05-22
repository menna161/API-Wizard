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


def http_get(url, temp_file, proxies=None, resume_size=0, user_agent=None):
    ua = 'transformers/{}; python/{}'.format(__version__, sys.version.split()[0])
    if is_torch_available():
        ua += '; torch/{}'.format(torch.__version__)
    if is_tf_available():
        ua += '; tensorflow/{}'.format(tf.__version__)
    if isinstance(user_agent, dict):
        ua += ('; ' + '; '.join(('{}/{}'.format(k, v) for (k, v) in user_agent.items())))
    elif isinstance(user_agent, str):
        ua += ('; ' + user_agent)
    headers = {'user-agent': ua}
    if (resume_size > 0):
        headers['Range'] = ('bytes=%d-' % (resume_size,))
    response = requests.get(url, stream=True, proxies=proxies, headers=headers)
    if (response.status_code == 416):
        return
    content_length = response.headers.get('Content-Length')
    total = ((resume_size + int(content_length)) if (content_length is not None) else None)
    progress = tqdm(unit='B', unit_scale=True, total=total, initial=resume_size, desc='Downloading', disable=bool((logger.getEffectiveLevel() == logging.NOTSET)))
    for chunk in response.iter_content(chunk_size=1024):
        if chunk:
            progress.update(len(chunk))
            temp_file.write(chunk)
    progress.close()
