import os
import unittest
import requests
import wget
from utility import Utility_object
from flexibox.core.logger import Logger


def testOperaDriverMac(self):
    driverAPI = self.parseJSONOpera()
    data = driverAPI.get('mac')
    download_url = self.parse_json(data)
    _response = requests.get(download_url)
    if (_response.status_code == 200):
        wget.download(download_url)
        self.log.log_info('Binary downloaded for mac')
    else:
        self.log.log_error('Connection error')
        raise requests.exceptions.ConnectionError('Connection error')
    self.assertTrue(os.path.exists('operadriver_mac64.zip'))
    self.log.log_info('Path for binary file exist')
    self.utility.delete_file('operadriver_mac64.zip')
    self.log.log_info('Binary files deleted')
