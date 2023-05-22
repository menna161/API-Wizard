import abc
import logging
import os
import os.path
from pathlib import Path
import platform
import shutil
import stat
import tarfile
import zipfile
from bs4 import BeautifulSoup
import requests
import tqdm
from .util import get_architecture_bitness
from urlparse import urlparse, urlsplit
from urllib.parse import urlparse, urlsplit


def _get_latest_version_number(self):
    resp = requests.get((self.chrome_driver_base_url + '/o/LATEST_RELEASE'))
    if (resp.status_code != 200):
        error_message = 'Error, unable to get version number for latest release, got code: {0}'.format(resp.status_code)
        logger.error(error_message)
        raise RuntimeError(error_message)
    latest_release = requests.get(resp.json()['mediaLink'])
    return latest_release.text
