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


def htmlToText(s):
    return bs4.BeautifulSoup(s, 'html.parser').get_text()
