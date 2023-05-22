import argparse
import collections
import glob
import hashlib
import json
import os
import pprint
import re
import shutil
import socket
import subprocess
import sys
import tempfile
import time
from concurrent.futures import ThreadPoolExecutor
from functools import partial
import apkutils2 as apkutils
import requests
import tornado.web
from logzero import logger
from tornado import gen, websocket
from tornado.concurrent import run_on_executor
from tornado.ioloop import IOLoop
from tornado.web import RequestHandler
from tornado.websocket import WebSocketHandler, websocket_connect
import adbutils
from adbutils import adb as adbclient
from asyncadb import adb
from device import STATUS_FAIL, STATUS_INIT, STATUS_OKAY, AndroidDevice
from heartbeat import heartbeat_connect
from core.utils import current_ip, fix_url, id_generator, update_recursive
from core import fetching
import uiautomator2 as u2
import settings
import traceback


@run_on_executor(executor='_download_executor')
def cache_download(self, url: str) -> str:
    ' download with local cache '
    target_path = self.cache_filepath(url)
    logger.debug('Download %s to %s', url, target_path)
    if os.path.exists(target_path):
        logger.debug('Cache hited')
        return target_path
    for fname in glob.glob('cache-*'):
        logger.debug('Remove old cache: %s', fname)
        os.unlink(fname)
    tmp_path = (target_path + '.tmp')
    r = requests.get(url, stream=True)
    r.raise_for_status()
    with open(tmp_path, 'wb') as tfile:
        content_length = int(r.headers.get('content-length', 0))
        if content_length:
            for chunk in r.iter_content(chunk_size=40960):
                tfile.write(chunk)
        else:
            shutil.copyfileobj(r.raw, tfile)
    os.rename(tmp_path, target_path)
    return target_path
