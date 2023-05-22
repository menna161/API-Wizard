import logging
from pip._vendor import requests
from pip._vendor.cachecontrol.adapter import CacheControlAdapter
from pip._vendor.cachecontrol.cache import DictCache
from pip._vendor.cachecontrol.controller import logger
from argparse import ArgumentParser


def get_session():
    adapter = CacheControlAdapter(DictCache(), cache_etags=True, serializer=None, heuristic=None)
    sess = requests.Session()
    sess.mount('http://', adapter)
    sess.mount('https://', adapter)
    sess.cache_controller = adapter.controller
    return sess
