import json
from collections import defaultdict
from pprint import pprint
import requests


def __init__(self, url_or_json: str):
    self.swagger_json = None
    if url_or_json.startswith('http'):
        self.swagger_json = requests.get(url_or_json).json()
    else:
        with open(url_or_json, encoding='utf-8') as f:
            self.swagger_json = json.loads(f.read())
    self.info = self.swagger_json['info']
    self.host = self.swagger_json['host']
    self.basePath = self.swagger_json['basePath']
    self.tags = self.swagger_json['tags']
    self.paths = self.swagger_json['paths']
    self.definitions = self.swagger_json['definitions']
