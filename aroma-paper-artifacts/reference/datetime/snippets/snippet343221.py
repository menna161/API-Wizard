import datetime
import time
import logging
import os
from pathlib import Path
from pymongo import MongoClient
import archon.broker.facade as facade
import archon.exchange.exchanges as exc
import archon.util.orderbooks as orderbooks
from archon.broker.config import parse_toml
from archon.feeds import cryptocompare
from archon.model import models
import archon.exchange.bitmex.fields as bitmexfields
from archon.util.custom_logger import setup_logger


def sync_orderbook(self, market, exchange):
    self.logger.debug(('sync %s %s' % (market, exchange)))
    try:
        n = exc.NAMES[exchange]
        book = self.afacade.get_orderbook(market, exchange)
        dt = datetime.datetime.utcnow()
        book['exchange'] = n
        self.logger.debug(('sync %s' % str(dt)))
        self.db.orderbooks.insert(book)
    except Exception as e:
        self.logger.info(('sync book failed %s' % e))
