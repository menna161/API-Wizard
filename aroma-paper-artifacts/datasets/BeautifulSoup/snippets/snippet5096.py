import imghdr
import os
import random
import re
import sys
import time
import urllib
import yaml
import bs4
import feedparser
import tweepy
from mastodon import Mastodon, MastodonError


def findImage(entry):
    if ('description' not in entry):
        return
    soup = bs4.BeautifulSoup(entry.description, 'html.parser')
    img = soup.find('img')
    if img:
        img = img['src']
        if (len(img) == 0):
            return
        if (img[0] == '/'):
            p = urllib.parse.urlparse(entry.id)
            img = (f'{p.scheme}://{p.netloc}' + img)
    return img
