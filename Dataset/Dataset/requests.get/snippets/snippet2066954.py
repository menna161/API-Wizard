from __future__ import print_function
import ast
import csv
import glob
import json
import logging
import os
import platform
import subprocess
import sys
import time
import ee
import pandas as pd
import requests
import retrying
from cerberus import Validator
from cerberus.errors import BasicErrorHandler
from natsort import natsorted
from requests_toolbelt import MultipartEncoder
from .metadata_loader import load_metadata_from_csv


def cookie_check(cookie_list):
    cook_list = []
    for items in cookie_list:
        cook_list.append('{}={}'.format(items['name'], items['value']))
    cookie = '; '.join(cook_list)
    headers = {'cookie': cookie}
    response = requests.get('https://code.earthengine.google.com/assets/upload/geturl', headers=headers)
    if ((response.status_code == 200) and (response.headers.get('content-type').split(';')[0] == 'application/json')):
        return True
    else:
        return False
