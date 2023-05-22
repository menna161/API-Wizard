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


def get_global_orderbook(self, market):
    books = list()
    for e in self.active_exchanges:
        n = exc.NAMES[e]
        self.logger.info(('global orderbook %s %s' % (n, market)))
        try:
            [bids, asks] = self.afacade.get_orderbook(market, e)
            dt = datetime.datetime.utcnow()
            n = exc.NAMES[e]
            for xb in bids:
                xb['exchange'] = n
            for xa in asks:
                xa['exchange'] = n
            x = {'market': market, 'exchange': n, 'bids': bids, 'asks': asks, 'timestamp': dt}
            books.append(x)
        except Exception as err:
            self.logger.error(('error global orderbook %s %s %s' % (e, market, err)))
    [bids, asks, ts] = orderbooks.aggregate_book(books)
    return [bids, asks, ts]
