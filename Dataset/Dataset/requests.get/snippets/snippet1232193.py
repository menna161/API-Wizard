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


def download(self, version='latest', os_name=None, bitness=None, show_progress_bar=True):
    '\n        Method for downloading a web driver binary.\n\n        :param version: String representing the version of the web driver binary to download.  For example, "2.38".\n                        Default if no version is specified is "latest".  The version string should match the version\n                        as specified on the download page of the webdriver binary.  Prior to downloading, the method\n                        will check the local filesystem to see if the driver has been downloaded already and will\n                        skip downloading if the file is already present locally.\n        :param os_name: Name of the OS to download the web driver binary for, as a str.  If not specified, we will use\n                        platform.system() to get the OS.\n        :param bitness: Bitness of the web driver binary to download, as a str e.g. "32", "64".  If not specified, we\n                        will try to guess the bitness by using util.get_architecture_bitness().\n        :param show_progress_bar: Boolean (default=True) indicating if a progress bar should be shown in the console.\n        :returns: The path + filename to the downloaded web driver binary.\n        '
    download_url = self.get_download_url(version, os_name=os_name, bitness=bitness)
    filename = os.path.split(urlparse(download_url).path)[1]
    filename_with_path = os.path.join(self.get_download_path(version), filename)
    if (not os.path.isdir(self.get_download_path(version))):
        os.makedirs(self.get_download_path(version))
    if os.path.isfile(filename_with_path):
        logger.info('Skipping download. File {0} already on filesystem.'.format(filename_with_path))
        return filename_with_path
    data = requests.get(download_url, stream=True)
    if (data.status_code == 200):
        logger.debug('Starting download of {0} to {1}'.format(download_url, filename_with_path))
        with open(filename_with_path, mode='wb') as fileobj:
            chunk_size = 1024
            if show_progress_bar:
                expected_size = int(data.headers['Content-Length'])
                for chunk in tqdm.tqdm(data.iter_content(chunk_size), total=int((expected_size / chunk_size)), unit='kb'):
                    fileobj.write(chunk)
            else:
                for chunk in data.iter_content(chunk_size):
                    fileobj.write(chunk)
        logger.debug('Finished downloading {0} to {1}'.format(download_url, filename_with_path))
        return filename_with_path
    else:
        error_message = 'Error downloading file {0}, got status code: {1}'.format(filename, data.status_code)
        logger.error(error_message)
        raise RuntimeError(error_message)
