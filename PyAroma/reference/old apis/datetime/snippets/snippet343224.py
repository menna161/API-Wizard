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


def sync_balances(self):
    balances = self.global_balances()
    self.logger.info(('insert %s' % balances))
    self.db.balances.drop()
    dt = datetime.datetime.utcnow()
    self.db.balances.insert({'balance_items': balances, 't': dt})
    self.db.balances_history.insert(balances)
