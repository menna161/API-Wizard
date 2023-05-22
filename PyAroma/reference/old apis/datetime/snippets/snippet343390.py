import time
import archon.broker as broker
import archon.facade as facade
from archon.util import *
import archon.mail as mail
import datetime
import schedule
import time


def order_report():
    '\n    market = "LTC_BTC"\n    oo = afacade.open_orders(market)\n    log.info("open orders " + str(oo))\n\n    txs = afacade.market_history(market)\n    log.info("txs " + str(txs[:3]))\n    \n    for tx in txs[:50]:\n        ts = tx[\'Timestamp\']\n        tsf = datetime.datetime.fromtimestamp(ts).strftime(\'%D %H:%M:%S\')\n        print (tx[\'Type\'],tsf)\n\n    [bids, asks] = afacade.get_orderbook(market)\n    log.info("bids " + str(bids[:3]))\n\n    usertx = afacade.trade_history(market)\n    print (usertx[:3])\n    '
