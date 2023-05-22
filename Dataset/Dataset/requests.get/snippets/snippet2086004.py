import os
import unittest
import requests
import wget
from utility import Utility_object
from flexibox.core.logger import Logger


@classmethod
def parse_json(self, api):
    response = requests.get(api)
    if (response.status_code == 200):
        data = response.json()
        return data['browser_download_url']
