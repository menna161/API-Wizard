from __future__ import print_function
import os
import tarfile
import requests
from warnings import warn
from zipfile import ZipFile
from bs4 import BeautifulSoup
from os.path import abspath, isdir, join, basename


@staticmethod
def _get_options(r):
    soup = BeautifulSoup(r.text, 'lxml')
    options = [h.text for h in soup.find_all('a', href=True) if h.text.endswith(('.zip', 'tar.gz'))]
    return options
