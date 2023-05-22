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


def __get_google_auth_session(username):
    ee.Initialize()
    platform_info = platform.system().lower()
    if ((str(platform_info) == 'linux') or (str(platform_info) == 'darwin')):
        subprocess.check_call(['stty', '-icanon'])
    if (not os.path.exists('cookie_jar.json')):
        try:
            cookie_list = raw_input('Enter your Cookie List:  ')
        except Exception:
            cookie_list = input('Enter your Cookie List:  ')
        finally:
            with open('cookie_jar.json', 'w') as outfile:
                json.dump(json.loads(cookie_list), outfile)
        cookie_list = json.loads(cookie_list)
    elif os.path.exists('cookie_jar.json'):
        with open('cookie_jar.json') as json_file:
            cookie_list = json.load(json_file)
        if (cookie_check(cookie_list) is True):
            print('Using saved Cookies')
            cookie_list = cookie_list
        elif (cookie_check(cookie_list) is False):
            try:
                cookie_list = raw_input('Cookies Expired | Enter your Cookie List:  ')
            except Exception:
                cookie_list = input('Cookies Expired | Enter your Cookie List:  ')
            finally:
                with open('cookie_jar.json', 'w') as outfile:
                    json.dump(json.loads(cookie_list), outfile)
                    cookie_list = json.loads(cookie_list)
    time.sleep(5)
    if (str(platform.system().lower()) == 'windows'):
        os.system('cls')
    elif (str(platform.system().lower()) == 'linux'):
        os.system('clear')
        subprocess.check_call(['stty', 'icanon'])
    elif (str(platform.system().lower()) == 'darwin'):
        os.system('clear')
        subprocess.check_call(['stty', 'icanon'])
    else:
        sys.exit(f'Operating system is not supported')
    session = requests.Session()
    for cookies in cookie_list:
        session.cookies.set(cookies['name'], cookies['value'])
    response = session.get('https://code.earthengine.google.com/assets/upload/geturl')
    if ((response.status_code == 200) and (ast.literal_eval(response.text)['url'] is not None)):
        return session
    else:
        print(response.status_code, response.text)
