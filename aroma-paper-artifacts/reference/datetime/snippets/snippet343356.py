import archon.exchange.cryptofacilities as cfApi
import datetime
import time
import archon.config as config
from datetime import datetime


def APITester():
    result = cfclient.get_tickers()
    print('get_tickers:\n', result)
    symbol = 'FI_XBTUSD_180615'
    result = cfclient.get_orderbook(symbol)
    print('get_orderbook:\n', result)
    '\n    symbol = "FI_XBTUSD_180615"  # "FI_XBTUSD_180615", "cf-bpi", "cf-hbpi"\n    lastTime = datetime.datetime.strptime("2016-01-20", "%Y-%m-%d").isoformat() + ".000Z"\n    result = cfclient.get_history(symbol, lastTime=lastTime)\n    print("get_history:\n", result)\n    '
    result = cfclient.get_openpositions()
    print('get_openpositions:\n', result)
