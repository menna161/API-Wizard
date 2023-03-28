from archon.util.custom_logger import setup_logger
from archon.exchange.bitmex.ws.api_util import generate_nonce, generate_signature
from archon.exchange.bitmex.ws.bitmex_topics import *
import websocket
import threading
import traceback
from time import sleep
import json
import urllib
import math
import pdb
import logging
import colorlog
import sys
from datetime import datetime


def __on_message(self, message, TESTXX):
    'Handler for parsing WS messages.'
    message = json.loads(message)
    self.msg_count += 1
    '\n        since_last = datetime.now() - self.last_msg\n        if self.msg_count%100==0:\n            ssec = since_last\n            print (ssec)\n            msg_rate = 100/ssec\n            print (self.msg_count, ssec, msg_rate)\n        '
    self.last_msg = datetime.now()
    self.handle_message(message)
