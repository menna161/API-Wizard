import os
from os.path import expanduser
import sys
import requests
import urllib
from PIL import ImageFile


def validURL(URL):
    statusCode = requests.get(URL, headers={'User-agent': 'getWallpapers'}).status_code
    if (statusCode == 404):
        return False
    else:
        return True
