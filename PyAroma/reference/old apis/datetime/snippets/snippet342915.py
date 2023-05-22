import sys
import os
import threading
import archon
import archon.facade as facade
import archon.broker as broker
import archon.exchange.exchanges as exc
import archon.markets as markets
import time
import datetime
import toml
import archon.model.models as models
from archon.util.custom_logger import setup_logger
import logging
from util import *
import random
import math


def submit_buy(self, price, qty):
    o = [self.market, 'BUY', price, qty]
    self.logger.info('submit ', o)
    [order_result, order_success] = self.afacade.submit_order(o, self.e)
    self.logger.info(order_result, order_success)
    if order_result:
        entry_time = datetime.now()
        position = [POSITION_LONG, market, price, entry_time]
        self.positions.append(position)
