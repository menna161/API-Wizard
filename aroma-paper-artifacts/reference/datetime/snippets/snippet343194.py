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


def __init__(self, setAuto=True, setMongo=True):
    setup_logger(logger_name='broker', log_file='broker.log')
    self.logger = logging.getLogger('broker')
    self.afacade = facade.Facade()
    self.balances = None
    self.openorders = list()
    self.submitted_orders = list()
    self.active_exchanges = list()
    self.selected_exchange = None
    if setAuto:
        self.set_keys_exchange_file()
    if setMongo:
        try:
            wdir = self.get_workingdir()
            path_file_config = ((wdir + '/') + 'config.toml')
            config_dict = parse_toml(path_file_config)
        except:
            self.logger.error(('no file. path expected: %s' % str(path_file_config)))
        try:
            mongo_conf = config_dict['MONGO']
            uri = mongo_conf['uri']
            self.set_mongo(uri)
            self.using_mongo = True
        except:
            self.using_mongo = False
            self.logger.error('could not set mongo')
    self.starttime = datetime.datetime.utcnow()
