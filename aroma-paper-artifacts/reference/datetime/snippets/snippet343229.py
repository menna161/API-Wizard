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


def sync_markets_all(self):
    self.db.markets.drop()
    ms = self.fetch_global_markets()
    dt = datetime.datetime.utcnow()
    nm = list()
    for x in ms:
        try:
            dts = dt.strftime('%H:%M:%S')
            x['timestamp'] = dts
            (n, d) = x['pair'].split('_')
            x['nom'] = n
            x['denom'] = d
            self.db.markets.insert(x)
            self.db.markets_history.insert(x)
        except:
            pass
