import os
from os.path import expanduser
import sys
import requests
import urllib
from PIL import ImageFile


def getPosts(subreddit, loops, after):
    allPosts = []
    i = 0
    while (i < loops):
        URL = 'https://reddit.com/r/{}/top/.json?t=all&limit={}&after={}'.format(subreddit, jsonLimit, after)
        posts = requests.get(URL, headers={'User-agent': 'getWallpapers'}).json()
        for post in posts['data']['children']:
            allPosts.append(post)
        after = posts['data']['after']
        i += 1
    return allPosts
