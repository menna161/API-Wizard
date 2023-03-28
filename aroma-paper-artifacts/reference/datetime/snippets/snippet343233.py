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


def sync_candle_minute15(self, market, exchange):
    self.logger.debug(('get candles %s %s ' % (market, str(exchange))))
    candles = self.afacade.get_candles_timeframe(market, exchange, self.acafade.TIMEFRAME_15MINUTE)
    n = exc.NAMES[exchange]
    [nom, denom] = models.market_parts(market)
    dt = datetime.datetime.utcnow()
    dts = dt.strftime('%H:%M:%S')
    self.db.candles.insert({'exchange': n, 'market': market, 'nom': nom, 'denom': denom, 'candles': candles, 'interval': '1m', 'time_insert': dts})
