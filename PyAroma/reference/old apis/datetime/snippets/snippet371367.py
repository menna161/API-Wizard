import bencode
import requests
import logging
import struct
import random
import socket
import threading
import datetime
import time
from threading import Thread
from . import utils
from .version import __version__
from urllib.parse import urlparse
from urlparse import urlparse


def downloading_message(self):
    if utils.timestamp_is_within_10_seconds(self.last_message_time):
        return
    self.last_message_time = int(datetime.datetime.timestamp(datetime.datetime.now()))
    resp = requests.models.Response()
    if (self.downloaded == 0):
        return True
    for tracker in self.torrent.trackers:
        if (tracker[0] == ''):
            continue
        elif (tracker[0][:4] == 'http'):
            params = {'info_hash': self.torrent.info_hash, 'peer_id': self.torrent.peer_id, 'uploaded': 0, 'downloaded': self.downloaded, 'left': (self.torrent.total_length - self.downloaded), 'port': 6881}
            try:
                resp = requests.get(tracker[0], params=params, timeout=30, headers={'user-agent': ((('AT-Client/' + __version__) + ' ') + requests.utils.default_user_agent())})
            except Exception as e:
                logging.info(e)
                pass
        return (params, resp)
