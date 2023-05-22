import logging
import json
import os
import random
import string
import sys
import pprint
import threading
import tempfile
import modules.urllib3 as urllib3
from urllib.parse import parse_qs
from typing import Dict, List
from http.server import HTTPServer, BaseHTTPRequestHandler
from enum import Enum
import modules.requests as requests


def get_installer(self):
    installer_path = os.path.join(tempfile.mkdtemp(), 'ffxivsetup.exe')
    resp = requests.get(self.INSTALL_URL)
    if (resp.status_code == 200):
        with open(installer_path, 'wb') as f:
            f.write(resp.content)
    return installer_path
