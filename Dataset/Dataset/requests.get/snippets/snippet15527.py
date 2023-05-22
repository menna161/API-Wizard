import json
import requests
import random
from lxml import html
from selenium import webdriver


def get_my_ip() -> str:
    url = 'https://api.ipify.org'
    reply = requests.get(url)
    assert (reply.status_code == 200)
    return reply.text
