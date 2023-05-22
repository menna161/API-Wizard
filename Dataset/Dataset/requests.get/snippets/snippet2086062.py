import os
import requests
from flexibox.core.logger import Logger
from flexibox.core.utility import Utility
from flexibox.utility.os_type import OS_type


def url_builder(self, os_extension):
    data = self.chromedriver_objects()
    LATEST_RELEASE = requests.get(data['latest_release'])
    url_builder = ((((((data['api_url'] + LATEST_RELEASE.text) + '/') + data['driver_type']) + os_extension) + data['arch']) + '.zip')
    return url_builder
