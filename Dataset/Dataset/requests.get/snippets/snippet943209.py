import fnmatch
from functools import wraps, partial
from hashlib import sha256
from io import open
import json
import logging
import os
import shutil
import tarfile
import tempfile
from torch.hub import _get_torch_home
from urllib.parse import urlparse
from pathlib import Path
import boto3
import boto3
import requests
import requests
from tqdm import tqdm
from urlparse import urlparse
from botocore.exceptions import ClientError
import requests


def http_get(url, temp_file):
    import requests
    from tqdm import tqdm
    req = request_wrap_timeout(partial(requests.get, url, stream=True), url)
    content_length = req.headers.get('Content-Length')
    total = (int(content_length) if (content_length is not None) else None)
    progress = tqdm(unit='B', total=total)
    for chunk in req.iter_content(chunk_size=1024):
        if chunk:
            progress.update(len(chunk))
            temp_file.write(chunk)
    progress.close()
