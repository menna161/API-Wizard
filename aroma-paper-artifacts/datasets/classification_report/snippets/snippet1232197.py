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
    '\n        Method for getting the download URL for the Gecko (Mozilla Firefox) driver binary.\n\n        :param version: String representing the version of the web driver binary to download.  For example, "v0.20.1".\n                        Default if no version is specified is "latest".  The version string should match the version\n                        as specified on the download page of the webdriver binary.\n        :param os_name: Name of the OS to download the web driver binary for, as a str.  If not specified, we will use\n                        platform.system() to get the OS.\n        :param bitness: Bitness of the web driver binary to download, as a str e.g. "32", "64".  If not specified, we\n                        will try to guess the bitness by using util.get_architecture_bitness().\n        :returns: The download URL for the Gecko (Mozilla Firefox) driver binary.\n        '
    if (version == 'latest'):
        gecko_driver_version_release_api_url = (self.gecko_driver_releases_api_url + version)
        gecko_driver_version_release_ui_url = (self.gecko_driver_releases_ui_url + version)
    else:
        gecko_driver_version_release_api_url = ((self.gecko_driver_releases_api_url + 'tags/') + version)
        gecko_driver_version_release_ui_url = ((self.gecko_driver_releases_ui_url + 'tags/') + version)
    logger.debug('Attempting to access URL: {0}'.format(gecko_driver_version_release_api_url))
    info = requests.get(gecko_driver_version_release_api_url)
    if (info.status_code != 200):
        info_message = 'Error, unable to get info for gecko driver {0} release. Status code: {1}'.format(version, info.status_code)
        logger.info(info_message)
        resp = requests.get(gecko_driver_version_release_ui_url, allow_redirects=True)
        if (resp.status_code == 200):
            json_data = {'assets': []}
        soup = BeautifulSoup(resp.text, features='html.parser')
        urls = [(resp.url + a['href']) for a in soup.find_all('a', href=True) if ('/download/' in a['href'])]
        for url in urls:
            json_data['assets'].append({'name': Path(urlsplit(url).path).name, 'browser_download_url': url})
    else:
        json_data = info.json()
    if (os_name is None):
        os_name = platform.system()
        if (os_name == 'Darwin'):
            os_name = 'macos'
        elif (os_name == 'Windows'):
            os_name = 'win'
        elif (os_name == 'Linux'):
            os_name = 'linux'
    if (bitness is None):
        bitness = get_architecture_bitness()
        logger.debug('Detected OS: {0}bit {1}'.format(bitness, os_name))
    filenames = [asset['name'] for asset in json_data['assets']]
    filename = [name for name in filenames if (os_name in name)]
    if (len(filename) == 0):
        info_message = 'Error, unable to find a download for os: {0}'.format(os_name)
        logger.error(info_message)
        raise RuntimeError(info_message)
    if (len(filename) > 1):
        filename = [name for name in filenames if ((os_name + bitness) in name)]
        if (len(filename) != 1):
            info_message = 'Error, unable to determine correct filename for {0}bit {1}'.format(bitness, os_name)
            logger.error(info_message)
            raise RuntimeError(info_message)
    filename = filename[0]
    result = json_data['assets'][filenames.index(filename)]['browser_download_url']
    logger.info('Download URL: {0}'.format(result))
    return result
