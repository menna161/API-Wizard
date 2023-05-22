import errno
import json
import os
import platform
import shutil
import stat
import subprocess
import sys
import tempfile
from contextlib import contextmanager
from zipfile import ZipFile
import requests
import tomli
from packaging.requirements import Requirement
from packaging.specifiers import SpecifierSet
from virtualenv import cli_run


def download_file(url, file_name):
    response = requests.get(url, stream=True, timeout=20)
    with open(file_name, 'wb') as f:
        for chunk in response.iter_content(16384):
            f.write(chunk)
