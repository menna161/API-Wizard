import os
import unittest
import requests
import wget
from utility import Utility_object
from flexibox.core.logger import Logger


def testGeckoDriverLinux64(self):
    _data = self.parseJSONResponse()
    _geckoBinLinux64DownloadURL = _data.get('linux_downloadURL_64')
    _geckoBinLinux64TagName = _data.get('linux_tagName_64')
    _response = requests.get(_geckoBinLinux64DownloadURL)
    self.assertEquals(_response.status_code, 200)
    self.log.log_info('Status code is 200')
    wget.download(_geckoBinLinux64DownloadURL)
    self.log.log_info('Binary for geckodriver downloaded for Linux 64 bit')
    self.assertTrue(os.path.exists(_geckoBinLinux64TagName))
    self.log.log_info('Path for binary file exist')
    self.utility.delete_file(_geckoBinLinux64TagName)
    self.log.log_info('Deleted required binaries')
