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


def get_download_path(self, version='latest'):
    if (version == 'latest'):
        info = requests.get((self.gecko_driver_releases_api_url + version))
        if (info.status_code != 200):
            info_message = 'Error attempting to get version info via API, got status code: {0}'.format(info.status_code)
            logger.info(info_message)
            resp = requests.get((self.gecko_driver_releases_ui_url + version))
            if (resp.status_code == 200):
                ver = Path(urlsplit(resp.url).path).name
        else:
            ver = info.json()['tag_name']
    else:
        ver = version
    return os.path.join(self.download_root, 'gecko', ver)
