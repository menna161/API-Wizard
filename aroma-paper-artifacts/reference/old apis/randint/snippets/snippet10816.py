import tweepy
import requests
import random
import time
import os
from boto.s3.connection import S3Connection


def select_image_path():
    nmr = random.randint(1, 31)
    image_path = (str(nmr) + '.jpg')
    return image_path
