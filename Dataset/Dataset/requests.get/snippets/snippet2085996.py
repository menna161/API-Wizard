import os
import unittest
import requests
import wget
from utility import Utility_object
from flexibox.core.logger import Logger


def testChromeDriverLinux(self):
    _data = self.parseJSONChrome()
    _releaseVersionAPI = _data.get('release_version')
    _releaseVersion = ''
    response = requests.get(_releaseVersionAPI)
    try:
        if (response.status_code == 200):
            _releaseVersion = response.text
    except requests.exceptions.Timeout:
        self.log.log_error('Request time out')
    except requests.exceptions.TooManyRedirects:
        self.log.log_error('Too many redirects')
    except requests.exceptions.RequestException as e:
        self.log.log_error(e)
    _url = _data.get('url')
    _linux_bin = _data.get('linux_v_64')
    _apiURLBuilder = (((_url + _releaseVersion) + '/') + _linux_bin)
    try:
        _url = requests.get(_apiURLBuilder)
        if (_url.status_code == 200):
            wget.download(_apiURLBuilder)
            self.log.log_info('Binary for chromedriver downloaded for Linux')
    except requests.exceptions.Timeout:
        self.log.log_error('Request time out')
    except requests.exceptions.TooManyRedirects:
        self.log.log_error('Too many redirects')
    except requests.exceptions.RequestException as e:
        self.log.log_error(e)
    self.assertTrue(os.path.exists('chromedriver_linux64.zip'))
    self.log.log_info('Required path for binary exist')
    self.utility.delete_file('chromedriver_linux64.zip')
    self.log.log_info('Deleted respective binary')
