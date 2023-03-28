import archon.exchange.exchanges as exc
import archon.feeds.cryptocompare as cryptocompare
import datetime
import pytz
from archon.util import *


def conv_timestamp_tx_dt(ts, exchange):
    target_format = '%Y-%m-%dT%H:%M:%S'
    if (exchange == exc.CRYPTOPIA):
        tsf = datetime.datetime.strptime(ts, '%Y-%m-%dT%H:%M:%S')
        utc = pytz.UTC
        utc_dt = tsf.astimezone(pytz.utc)
        return utc_dt
    elif (exchange == exc.BITTREX):
        ts = ts.split('.')[0]
        tsf = datetime.datetime.strptime(ts, '%Y-%m-%dT%H:%M:%S')
        utc = pytz.UTC
        utc_dt = tsf.astimezone(pytz.utc)
        utc_dt = (utc_dt + datetime.timedelta(hours=4))
        return utc_dt
    elif (exchange == exc.KUCOIN):
        tsf = datetime.datetime.utcfromtimestamp(ts)
        utc = pytz.UTC
        utc_dt = tsf.astimezone(pytz.utc)
        utc_dt = (utc_dt + datetime.timedelta(hours=2))
        return utc_dt
    elif (exchange == exc.HITBTC):
        ts = ts[:(- 5)]
        x = datetime.datetime.strptime(ts, '%Y-%m-%dT%H:%M:%S')
        utc_dt = x.astimezone(pytz.utc)
        utc_dt = (utc_dt + datetime.timedelta(hours=2))
        return utc_dt
    elif (exchange == exc.BINANCE):
        tsf = datetime.datetime.utcfromtimestamp(int((ts / 1000)))
        utc = pytz.UTC
        utc_dt = tsf.astimezone(pytz.utc)
        utc_dt = (utc_dt + datetime.timedelta(hours=2))
        return utc_dt
