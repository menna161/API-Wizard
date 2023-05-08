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


def getPeersFromTrackers(self):
    if utils.timestamp_is_within_10_seconds(self.last_update_time):
        return
    self.last_update_time = int(datetime.datetime.timestamp(datetime.datetime.now()))
    for tracker in self.torrent.trackers:
        if (tracker[0] == ''):
            continue
        elif (tracker[0][:4] == 'http'):
            t1 = FuncThread(self.scrapeHTTP, self.torrent, tracker[0])
            self.lstThreads.append(t1)
            t1.start()
        else:
            t2 = FuncThread(self.scrape_udp, self.torrent, tracker[0])
            self.lstThreads.append(t2)
            t2.start()
    for t in self.lstThreads:
        t.join()
