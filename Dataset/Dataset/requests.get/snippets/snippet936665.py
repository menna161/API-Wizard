import shutil
import tarfile
import tempfile
import zipfile
import humanize
import progress.bar
import requests
from logzero import logger
from uiautomator2.version import __atx_agent_version__


def download(url: str, storepath: str):
    r = requests.get(url, stream=True)
    r.raise_for_status()
    file_size = int(r.headers.get('Content-Length'))
    bar = DownloadBar(storepath, max=file_size)
    chunk_length = (16 * 1024)
    with open((storepath + '.part'), 'wb') as f:
        for buf in r.iter_content(chunk_length):
            f.write(buf)
            bar.next(len(buf))
        bar.finish()
    shutil.move((storepath + '.part'), storepath)
