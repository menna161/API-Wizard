from __future__ import print_function
import os
import tarfile
import requests
from warnings import warn
from zipfile import ZipFile
from bs4 import BeautifulSoup
from os.path import abspath, isdir, join, basename


def _present_options(self):
    r = requests.get(self.url)
    options = self._get_options(r)
    print('Options:\n')
    for (i, o) in enumerate(options):
        print('{0}: {1}'.format(i, o))
    choice = input('\nPlease enter the number of the dataset above you wish to download:')
    return options[int(choice)]
