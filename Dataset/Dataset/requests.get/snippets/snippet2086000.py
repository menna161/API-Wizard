import os
import unittest
import requests
import wget
from utility import Utility_object
from flexibox.core.logger import Logger


def testGeckoDriverMac(self):
    _data = self.parseJSONResponse()
    _geckoBinMacDownloadURL = _data.get('mac_downloadURL')
    _geckoBinMacTagName = _data.get('mac_tagName')
    print(_geckoBinMacTagName)
    _response = requests.get(_geckoBinMacDownloadURL)
    self.assertEquals(_response.status_code, 200)
    self.log.log_info('Response status code is 200')
    wget.download(_geckoBinMacDownloadURL)
    self.log.log_info('Binary for geckodriver downloaded for macOS')
    self.assertTrue(os.path.exists(_geckoBinMacTagName))
    self.log.log_info('Path for binary exist')
    self.utility.delete_file(_geckoBinMacTagName)
    self.log.log_info('Binary files deleted')
