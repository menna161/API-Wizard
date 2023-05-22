import os
import unittest
import requests
import wget
from utility import Utility_object
from flexibox.core.logger import Logger


def parseJSONResponse(self):
    linux_downloadURL_32 = None
    linux_downloadURL_64 = None
    mac_downloadURL = None
    linux_tagName_32 = None
    linux_tagName_64 = None
    mac_tagName = None
    env = {}
    _response = requests.get(self.parseJSONGecko())
    if (_response.status_code == 200):
        data = _response.json()
        for ent in data['assets']:
            if ('linux32.tar.gz' in ent['browser_download_url']):
                linux_downloadURL_32 = ent['browser_download_url']
                linux_tagName_32 = ent['name']
            if ('linux64.tar.gz' in ent['browser_download_url']):
                linux_downloadURL_64 = ent['browser_download_url']
                linux_tagName_64 = ent['name']
            if ('macos.tar.gz' in ent['browser_download_url']):
                mac_downloadURL = ent['browser_download_url']
                mac_tagName = ent['name']
    env = {'linux_downloadURL_32': linux_downloadURL_32, 'linux_tagName_32': linux_tagName_32, 'linux_downloadURL_64': linux_downloadURL_64, 'linux_tagName_64': linux_tagName_64, 'mac_downloadURL': mac_downloadURL, 'mac_tagName': mac_tagName}
    return env
