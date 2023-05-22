import os
from os.path import expanduser
import sys
import requests
import urllib
from PIL import ImageFile


def verifySubreddit(subreddit):
    URL = 'https://reddit.com/r/{}.json'.format(subreddit)
    result = requests.get(URL, headers={'User-agent': 'getWallpapers'}).json()
    try:
        result['error']
        return False
    except:
        return True
