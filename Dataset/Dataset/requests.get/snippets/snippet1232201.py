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


def get_download_url(self, version='latest', os_name=None, bitness=None):
    '\n        Method for getting the download URL for the Google Chome driver binary.\n\n        :param version: String representing the version of the web driver binary to download.  For example, "2.39".\n                        Default if no version is specified is "latest".  The version string should match the version\n                        as specified on the download page of the webdriver binary.\n        :param os_name: Name of the OS to download the web driver binary for, as a str.  If not specified, we will use\n                        platform.system() to get the OS.\n        :param bitness: Bitness of the web driver binary to download, as a str e.g. "32", "64".  If not specified, we\n                        will try to guess the bitness by using util.get_architecture_bitness().\n        :returns: The download URL for the Google Chrome driver binary.\n        '
    if (version == 'latest'):
        version = self._get_latest_version_number()
    if (os_name is None):
        os_name = platform.system()
        if (os_name == 'Darwin'):
            os_name = 'mac'
        elif (os_name == 'Windows'):
            os_name = 'win'
        elif (os_name == 'Linux'):
            os_name = 'linux'
    if (bitness is None):
        bitness = get_architecture_bitness()
        logger.debug('Detected OS: {0}bit {1}'.format(bitness, os_name))
    chrome_driver_objects = requests.get((self.chrome_driver_base_url + '/o'))
    matching_versions = [item for item in chrome_driver_objects.json()['items'] if item['name'].startswith(version)]
    os_matching_versions = [item for item in matching_versions if (os_name in item['name'])]
    if (not os_matching_versions):
        error_message = 'Error, unable to find appropriate download for {0}.'.format((os_name + bitness))
        logger.error(error_message)
        raise RuntimeError(error_message)
    elif (len(os_matching_versions) == 1):
        result = os_matching_versions[0]['mediaLink']
    elif (len(os_matching_versions) == 2):
        result = [item for item in matching_versions if ((os_name + bitness) in item['name'])][0]['mediaLink']
    return result
