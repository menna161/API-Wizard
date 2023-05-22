import random
import string
import codecs
from os import path
import traceback
import ast
from re import sub
import requests
from pathlib import Path
import time
import numpy as np
from typing import Tuple, List
from IPython import get_ipython
from IPython.core.debugger import set_trace
from b2.constants import ISDEBUG
from b2.util.errors import UserError, InternalLogicalError
import folium
import folium.plugins


def fetch_and_cache(data_url, file, data_dir='data', force=False):
    '\n    Download and cache a url and return the file object.\n    \n    data_url: the web address to download\n    file: the file in which to save the results.\n    data_dir: (default="data") the location to save the data\n    force: if true the file is always re-downloaded \n    \n    return: The pathlib.Path object representing the file.\n    '
    data_dir = Path(data_dir)
    data_dir.mkdir(exist_ok=True)
    file_path = (data_dir / Path(file))
    if (force and file_path.exists()):
        file_path.unlink()
    if (force or (not file_path.exists())):
        print('Downloading...', end=' ')
        resp = requests.get(data_url)
        with file_path.open('wb') as f:
            f.write(resp.content)
        print('Done!')
        last_modified_time = time.ctime(file_path.stat().st_mtime)
    else:
        last_modified_time = time.ctime(file_path.stat().st_mtime)
        print('Using cached version that was downloaded (UTC):', last_modified_time)
    return file_path
