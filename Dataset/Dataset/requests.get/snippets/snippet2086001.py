import os
import unittest
import requests
import wget
from utility import Utility_object
from flexibox.core.logger import Logger


def testGeckoDriverLinux32(self):
    _data = self.parseJSONResponse()
    _geckoBinLinux32DownloadURL = _data.get('linux_downloadURL_32')
    _geckoBinLinux32TagName = _data.get('linux_tagName_32')
    _response = requests.get(_geckoBinLinux32DownloadURL)
    self.assertEquals(_response.status_code, 200)
    self.log.log_info('Response status code is 200')
    wget.download(_geckoBinLinux32DownloadURL)
    self.log.log_info('Binary for geckodriver downloaded for Linux 32 bit')
    self.assertTrue(os.path.exists(_geckoBinLinux32TagName))
    self.log.log_info('Path for binary exists')
    self.utility.delete_file(_geckoBinLinux32TagName)
    self.log.log_info('Binary files have been deleted')
