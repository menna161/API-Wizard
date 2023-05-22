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


def __init__(self, symbol, api_key=None, api_secret=None, redis_client=None):
    'Connect to the websocket and initialize data stores.'
    setup_logger(__name__, 'strategy.log')
    self.logger = logging.getLogger(__name__)
    self.logger.debug('bitmex - initializing WebSocket.')
    self.endpoint = endpoint_V1
    self.symbol = symbol
    self.msg_processed = 0
    if ((api_key is not None) and (api_secret is None)):
        raise ValueError('api_secret is required if api_key is provided')
    self.api_key = api_key
    self.api_secret = api_secret
    self.redis_client = redis_client
    self.data = {}
    self.keys = {}
    self.exited = False
    self.orderbook = {}
    self.msg_count = 0
    self.last_msg = datetime.now()
    self.symbolSubs = [TOPIC_instrument, TOPIC_orderBook10, TOPIC_quote, TOPIC_trade]
    self.genericSubs = [TOPIC_margin]
    symbol_subscriptions = [((sub + ':') + self.symbol) for sub in self.symbolSubs]
    self.subscriptions = (symbol_subscriptions + self.genericSubs)
    self.logger.info(('subscriptions %s' % str(self.subscriptions)))
    self.all_topics = (self.symbolSubs + self.genericSubs)
    self.subscribed = list()
    wsURL = self.__get_url()
    self.logger.info(('Connecting to %s' % wsURL))
    self.__connect(wsURL, symbol)
    self.logger.info('Connected to WS.')
    self.logger.info('Wait for initial data')
    self.got_init_data = False
    self.got_init_data = True
    self.logger.info('Got all market data. Starting.')
