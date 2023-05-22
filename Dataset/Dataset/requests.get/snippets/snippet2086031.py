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


def api_parser(self, api_url):
    try:
        response = None
        request_api = requests.get(api_url)
        if (request_api.status_code == 200):
            request = requests.get(api_url)
            response = request.json()
            return response
        else:
            request.raise_for_status()
    except requests.exceptions.Timeout:
        self.log.log_error('Request time out encountered')
    except requests.exceptions.TooManyRedirects:
        self.log.log_error('Too many redirects encountered')
    except requests.exceptions.HTTPError:
        self.log.log_error('HTTP error encountered')
        sys.exit(1)
