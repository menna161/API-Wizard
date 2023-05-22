import os
import shutil
import tarfile
import tempfile
import zipfile
import humanize
import requests
from logzero import logger
from uiautomator2.version import __apk_version__, __atx_agent_version__
import settings


def download(url: str, storepath: str):
    target_dir = (os.path.dirname(storepath) or '.')
    os.makedirs(target_dir, exist_ok=True)
    r = requests.get(url, stream=True)
    r.raise_for_status()
    total_size = int(r.headers.get('Content-Length', '-1'))
    bytes_so_far = 0
    prefix = ('Downloading %s' % os.path.basename(storepath))
    chunk_length = (16 * 1024)
    with open((storepath + '.part'), 'wb') as f:
        for buf in r.iter_content(chunk_length):
            bytes_so_far += len(buf)
            print(f'''
{prefix} {bytes_so_far} / {total_size}''', end='', flush=True)
            f.write(buf)
        print(' [Done]')
    if ((total_size != (- 1)) and (os.path.getsize((storepath + '.part')) != total_size)):
        raise ValueError('download size mismatch')
    shutil.move((storepath + '.part'), storepath)
