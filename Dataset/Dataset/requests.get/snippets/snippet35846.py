from __future__ import division
from __future__ import print_function
import base64
import ConfigParser
import hashlib
import inspect
import json
import os
import platform
import plistlib
import pwd
import re
import socket
import subprocess
import sys
import tkFileDialog
import tkSimpleDialog
import ttk
from Tkinter import Tk, N, E, S, W, StringVar, IntVar, PhotoImage, HORIZONTAL
import logging
import pexpect
import requests
import mount_shares_better as msb


def verify_network(self):
    '\n        Verifies network availability.\n\n        Host: 8.8.8.8 (google-public-dns-a.google.com)\n        OpenPort: 53/tcp\n        Service: domain (DNS/TCP)\n        '
    try:
        _ = requests.get('https://dns.google.com', timeout=3)
        return True
    except requests.ConnectionError as exception_message:
        self.logger.error(('%s: Unknown error. [%s]' % (inspect.stack()[0][3], exception_message)))
    return False
