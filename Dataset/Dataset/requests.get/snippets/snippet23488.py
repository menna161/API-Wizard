from typing import Union, List
import hashlib
import io
import os
import re
import textwrap
from os import getcwd, listdir, walk
from os.path import isfile, splitext, isdir, join, basename
from urllib.parse import urlparse
import click
import iscc
import requests
from PIL import Image
import iscc_cli
from iscc_cli.const import SUPPORTED_EXTENSIONS, SUPPORTED_MIME_TYPES, ISCC_COMPONENT_CODES, GMT


def download_file(url, md5=None, sanitize=False):
    'Download file to app dir and return path.'
    url_obj = urlparse(url)
    file_name = (os.path.basename(url_obj.path) or 'temp.file')
    if sanitize:
        file_name = safe_filename(file_name)
    out_path = os.path.join(iscc_cli.APP_DIR, file_name)
    if os.path.exists(out_path):
        click.echo(('Already downloaded: %s' % file_name))
        if md5:
            md5_calc = hashlib.md5(open(out_path, 'rb').read()).hexdigest()
            assert (md5 == md5_calc)
        return out_path
    r = requests.get(url, stream=True)
    length = int(r.headers['content-length'])
    chunk_size = 512
    iter_size = 0
    with io.open(out_path, 'wb') as fd:
        with click.progressbar(length=length, label=('Downloading %s' % file_name)) as bar:
            for chunk in r.iter_content(chunk_size):
                fd.write(chunk)
                iter_size += chunk_size
                bar.update(chunk_size)
    if md5:
        md5_calc = hashlib.md5(open(out_path, 'rb').read()).hexdigest()
        assert (md5 == md5_calc)
    return out_path
