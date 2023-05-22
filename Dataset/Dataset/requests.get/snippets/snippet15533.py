import os
import re
import time
import stat
import subprocess
import platform
import requests
from lxml import html
from zipfile import ZipFile
from urllib.parse import urlparse, urlunparse


def get_latest_release(version: str) -> str:
    main_version = version.split('.')[0]
    url = f'https://chromedriver.storage.googleapis.com/LATEST_RELEASE_{main_version}'
    reply = requests.get(url)
    assert (reply.status_code == 200)
    latest_relase = reply.text
    return latest_relase
