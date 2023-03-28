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


def sync_tx(self, market, exchange):
    try:
        smarket = models.conv_markets_to(market, exchange)
        txs = self.afacade.market_history(smarket, exchange)
        n = exc.NAMES[exchange]
        smarket = models.conv_markets_to(market, exchange)
        dt = datetime.datetime.utcnow()
        x = {'market': market, 'exchange': n, 'tx': txs, 'timestamp': dt}
        self.db.txs.remove({'market': market, 'exchange': n})
        self.db.txs.insert(x)
        self.db.txs_history.insert(x)
    except:
        self.logger.error('symbol not supported')
