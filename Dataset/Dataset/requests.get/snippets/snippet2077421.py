import os
import re
import logging
import subprocess
import datetime as dt
from time import sleep
import requests
from pyedgar import config
from pyedgar import utilities


def download_from_edgar(edgar_url, local_path, overwrite=False, use_requests=False, chunk_size=(10 * (1024 ** 2)), overwrite_size_threshold=(- 1), sleep_after=0, force_make_index_cache_directory=True):
    '\n    Generic downloader, uses curl by default unless use_requests=True is passed in.\n\n    Arguments:\n        edgar_url (str): URL of EDGAR resource.\n        local_path (Path, str): Local path to write to\n        overwrite (bool): Flag for whether to overwrite any existing file (default False).\n        use_requests (bool): Flag for whether to use requests or curl (default False == curl).\n        chunk_size (int): Size of chunks to write to disk while streaming from requests\n        overwrite_size_threshold (int): Existing files smaller than this will be re-downloaded.\n        sleep_after (int): Number of seconds to sleep after downloading file (default 0)\n\n    Returns:\n        (str, None): Returns path of downloaded file (or None if download failed).\n    '
    if (not os.path.exists(os.path.dirname(local_path))):
        if force_make_index_cache_directory:
            os.makedirs(os.path.dirname(local_path))
        else:
            raise FileNotFoundError('Trying to write to non-existant directory: {}'.format(os.path.dirname(local_path)))
    if os.path.exists(local_path):
        loc_size = os.path.getsize(local_path)
        if ((not overwrite) and (loc_size > overwrite_size_threshold)):
            _logger.info('Skipping cache file (%s bytes) at %r', '{:,d}'.format(loc_size), local_path)
            return local_path
        _logger.warning('Removing existing file (%s bytes) at %r', '{:,d}'.format(loc_size), local_path)
        os.remove(local_path)
    _useragent = REQUEST_HEADERS['User-Agent']
    if (not use_requests):
        _logger.debug('curl -A "%s" %s -o %s', _useragent, edgar_url, local_path)
        subp = use_subprocess(['curl', '-A "{}"'.format(_useragent), edgar_url, '-o', local_path])
        _logger.debug(subp.stdout)
        sleep(sleep_after)
        if (subp.returncode != 0):
            raise Exception('Error {} downloading with curl: {}'.format(subp.returncode, subp.stderr))
    else:
        _logger.debug('requests.get(%r, headers=%r) >> %r', edgar_url, REQUEST_HEADERS, local_path)
        try:
            with requests.get(edgar_url, headers=REQUEST_HEADERS, stream=True) as response:
                expected_len = int(response.headers['content-length'])
                with open(local_path, 'wb') as fh:
                    for chunk in response.iter_content(chunk_size=chunk_size):
                        if chunk:
                            fh.write(chunk)
            sleep(sleep_after)
        except Exception as excp:
            raise Exception('Error downloading with requests: {}'.format(excp)) from excp
        try:
            loc_size = os.path.getsize(local_path)
        except FileNotFoundError:
            raise Exception('Error downloading with requests to: {}'.format(local_path))
        if (expected_len != loc_size):
            _logger.exception('requests downloaded {:,d} bytes but expected {:,d}'.format(loc_size, expected_len))
    if os.path.exists(local_path):
        _logger.info('Done downloading %.3f MB to %s', (os.path.getsize(local_path) / (1024 ** 2)), local_path)
        return local_path
    return None
