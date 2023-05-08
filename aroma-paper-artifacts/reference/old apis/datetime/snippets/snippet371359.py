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


def __init__(self, torrent, new_peers_queue, downloaded):
    Thread.__init__(self)
    self.torrent = torrent
    self.lstThreads = []
    self.new_peers_queue = new_peers_queue
    self.stop_requested = False
    self.downloaded = downloaded
    self.last_message_time = int(datetime.datetime.timestamp(datetime.datetime.now()))
    self.last_update_time = int(datetime.datetime.timestamp(datetime.datetime.now()))
