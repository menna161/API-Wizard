import json
import os
import shutil
import stat
import sys
import tarfile
from configparser import SafeConfigParser
from datetime import datetime
from time import sleep
from zipfile import ZipFile
import requests
import wget
from flexibox.core.logger import Logger


def driver_downloader(self, api_url, dir_path):
    try:
        request_api = requests.get(api_url, stream=True)
        if (request_api.status_code == 200):
            wget.download(api_url, out=dir_path)
        else:
            request_api.raise_for_status()
    except requests.exceptions.Timeout:
        self.log.log_error('Request time out encountered')
    except requests.exceptions.TooManyRedirects:
        self.log.log_error('Too many redirects encountered')
    except requests.exceptions.HTTPError as e:
        self.log.log_error(e)
        sys.exit(1)
