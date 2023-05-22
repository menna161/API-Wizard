from datetime import date, datetime
from enum import Enum
import json
import logging
import posixpath
import socket
import struct
import time
from urllib.parse import urlparse, urlunparse
import requests
import urllib3
from isilon_hadoop_tools import IsilonHadoopToolError
import isi_sdk_8_2_2
import isi_sdk_7_2
import isi_sdk_8_0
import isi_sdk_8_0_1
import isi_sdk_8_1_0
import isi_sdk_8_1_1
import isi_sdk_8_2_0
import isi_sdk_8_2_1
import isi_sdk_8_2_2


def check_license(self, name):
    "Check for a license on OneFS and raise a MissingLicenseError if it doesn't exist."
    [license_] = self._license(name).licenses
    if (not _license_is_active(license_)):
        if (license_.expiration and (datetime.strptime(license_.expiration, '%Y-%m-%d').date() < date.today())):
            raise ExpiredLicenseError(name)
        raise MissingLicenseError(name)
