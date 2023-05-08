from __future__ import print_function
import os
import os.path
import re
import time
import sys
import hashlib
import json
import difflib
import tempfile
from datetime import datetime
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.errorhandler import NoSuchElementException
from xml.etree import ElementTree
from colorama import Fore, Back, Style


def set_modified(self, filename, modified=None):
    if (modified is None):
        modified = datetime.now().strftime('%d/%m/%Y')
    self.set(filename, 'modified', modified)
