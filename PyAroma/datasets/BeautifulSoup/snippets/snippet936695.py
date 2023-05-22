from requests import get
from packaging import version
from src import config
from src import common_utils
import git
import os
import sys
import shutil
import logging
import requests
from bs4 import BeautifulSoup
import apt


def get_src_rpm_filename(url, src_version):
    try:
        response = requests.get(url, timeout=5)
    except Exception as e:
        logger.error(e)
        sys.exit(1)
    if response.ok:
        response_text = response.text
        soup = BeautifulSoup(response_text, 'html.parser')
        for node in soup.find_all('a'):
            if (node.get('href').endswith('rpm') and ('nginx-{}-'.format(src_version) in node.get('href'))):
                file_name = node.get('href')
    elif (400 <= response.status_code < 500):
        logger.error(u'{} Client Error: {} for url: {}'.format(response.status_code, response.reason, url))
        sys.exit(1)
    elif (500 <= response.status_code < 600):
        logger.error(u'{} Server Error: {} for url: {}'.format(response.status_code, response.reason, url))
        sys.exit(1)
    if ('file_name' in locals()):
        return file_name
    else:
        logger.error('Cannot find nginx source rpm(SRPM) with version {} in url {}'.format(src_version, url))
        sys.exit(1)
