import json
import os
import datetime
import time
from pymongo import MongoClient
import logging
import redis
from archon.broker.config import *
import archon.brokersrv.facader as facader
import archon.exchange.exchanges as exc
from archon.model import models
import archon.util.orderbooks as orderbooks
from archon.feeds import cryptocompare
from archon.util import *
import archon.exchange.bitmex.fields as bitmexfields
from archon.exchange.bitmex.ws.bitmex_ws import BitMEXWebsocket
from archon.util.custom_logger import setup_logger, remove_loggers
import archon.exchange.bitmex.bitmex as mex
from .feeder import Feeder
from .topics import *
from pathlib import Path


def __init__(self, setAuto=True, setMongo=True, setRedis=True, initFeeder=True):
    setup_logger(logger_name='brokerservice', log_file='brokerservice.log')
    self.logger = logging.getLogger('brokerservice')
    self.afacade = facader.FacadeRaw()
    self.balances = None
    conf_file = 'conf.toml'
    wdir = self.get_workingdir()
    keys_filename = standard_conf_file
    path_file_conf = ((wdir + '/') + keys_filename)
    if setAuto:
        self.set_keys_exchange_file()
    if (not os.path.exists(path_file_conf)):
        self.logger.error(('no toml file. expected path %s' % str(path_file_conf)))
    else:
        try:
            all_conf = parse_toml(path_file_conf)
        except:
            self.logger.error(('config file %s not properly formatted' % str(conf_file)))
    if setMongo:
        try:
            mongo_conf = all_conf['MONGO']
            self.logger.info(('mongo conf %s' % str(mongo_conf)))
            uri = mongo_conf['uri']
            self.set_mongo(uri)
            self.using_mongo = True
        except Exception as e:
            self.using_mongo = False
            self.logger.error('could not set mongo. wrong configuration or config file')
            self.logger.error(str(e))
    self.starttime = datetime.datetime.utcnow()
    self.logger.info('Init feeder stream')
    if setRedis:
        self.logger.info(all_conf)
        try:
            redis_conf = all_conf['REDIS']
            host = redis_conf['host']
            port = redis_conf['port']
            self.redis_client = redis.Redis(host=host, port=port)
        except Exception as e:
            self.logger.error(('could not set redis %s %s' % (str(host), str(port))))
            self.logger.error(str(e))
    if initFeeder:
        f = Feeder(self)
        f.start()
        f.join()
