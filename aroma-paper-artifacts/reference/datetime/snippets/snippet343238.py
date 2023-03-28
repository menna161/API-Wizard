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


def transaction_queue(self, exchange):
    now = datetime.datetime.utcnow()
    txs = self.afacade.get_tradehistory_all(exchange)
    for tx in txs[:]:
        ts = tx['timestamp'][:19]
        dt = datetime.datetime.strptime(ts, '%Y-%m-%dT%H:%M:%S')
        if (dt > self.starttime):
            self.logger.info('new tx')
