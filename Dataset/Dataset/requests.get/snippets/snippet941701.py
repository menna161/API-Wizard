from __future__ import print_function
import os
import tarfile
import requests
from warnings import warn
from zipfile import ZipFile
from bs4 import BeautifulSoup
from os.path import abspath, isdir, join, basename


def _download_data(self, dataset_url, save_path):
    if (not isdir(save_path)):
        os.makedirs(save_path)
    base = basename(dataset_url)
    temp_save_path = join(save_path, base)
    with open(temp_save_path, 'wb') as f:
        r = requests.get(dataset_url)
        f.write(r.content)
    if base.endswith('.tar.gz'):
        obj = tarfile.open(temp_save_path)
    elif base.endswith('.zip'):
        obj = ZipFile(temp_save_path, 'r')
    else:
        raise ValueError('Unknown File Type: {0}.'.format(base))
    self._print('Unpacking Data...')
    obj.extractall(save_path)
    obj.close()
    os.remove(temp_save_path)
