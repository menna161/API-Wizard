import sys
import archon.facade as facade
import archon.broker as broker
import archon.exchange.exchanges as exc
import time
import datetime
from archon.util import *
from util import *
import math


def user_tx():
    a = broker.Broker()
    ae = [exc.BINANCE]
    a.set_active_exchanges(ae)
    txs = a.global_tradehistory()
    print('len ', len(txs))
    for tx in txs[:]:
        print(tx)
    '\n    for tx in txs[:]:        \n        #print (tx)\n        ts = tx[\'timestamp\'][:19]\n        timestamp_from = datetime.datetime.strptime(ts, \'%Y-%m-%dT%H:%M:%S\')        \n        #tx["timestamp"] = timestamp_from\n        m = tx[\'market\']        \n        tday = timestamp_from.day        \n        #print (tx)\n        if tday>20:\n            r = tx[\'price\']\n            a = tx[\'quantity\']\n            ty = tx[\'txtype\']\n            #print (m,r,a,ty)\n    '
