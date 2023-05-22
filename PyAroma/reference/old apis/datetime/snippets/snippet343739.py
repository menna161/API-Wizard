import archon.exchange.exchanges as exc
import archon.feeds.cryptocompare as cryptocompare
import datetime
import pytz
from archon.util import *


def conv_orderbook(book, exchange):
    if (exchange == exc.CRYPTOPIA):
        bids = book['Buy']
        asks = book['Sell']
        rate_key = book_key_price(exchange)
        qty_key = book_key_qty(exchange)
        newb = list()
        for b in bids:
            order = {'price': b[rate_key], 'quantity': b[qty_key]}
            newb.append(order)
        newa = list()
        for a in asks:
            order = {'price': a[rate_key], 'quantity': a[qty_key]}
            newa.append(order)
        return [newb, newa]
    elif (exchange == exc.BITTREX):
        bids = book['buy']
        asks = book['sell']
        rate_key = book_key_price(exchange)
        qty_key = book_key_qty(exchange)
        newb = list()
        for b in bids:
            newb.append({'price': b[rate_key], 'quantity': b[qty_key]})
        newa = list()
        for a in asks:
            newa.append({'price': a[rate_key], 'quantity': a[qty_key]})
        return [newb, newa]
    elif (exchange == exc.KUCOIN):
        bids = book['BUY']
        asks = book['SELL']
        newb = list()
        for b in bids:
            (p, v, t) = b
            d = {'price': p, 'quantity': v}
            newb.append(d)
        newa = list()
        for a in asks:
            (p, v, t) = a
            d = {'price': p, 'quantity': v}
            newa.append(d)
        book = [newb, newa]
        return book
    elif (exchange == exc.HITBTC):
        bids = book['bid']
        asks = book['ask']
        newb = list()
        for b in bids:
            (p, v) = (float(b['price']), float(b['size']))
            d = {'price': p, 'quantity': v}
            newb.append(d)
        newa = list()
        for a in asks:
            (p, v) = (float(a['price']), float(a['size']))
            d = {'price': p, 'quantity': v}
            newa.append(d)
        book = [newb, newa]
        return book
    elif (exchange == exc.KRAKEN):
        bids = book['bids']
        asks = book['asks']
        newb = list()
        for b in bids:
            (p, v, ts) = (float(b[0]), float(b[1]), b[2])
            d = {'price': p, 'quantity': v}
            newb.append(d)
        newa = list()
        for a in asks:
            (p, v, ts) = (float(a[0]), float(a[1]), a[2])
            d = {'price': p, 'quantity': v}
            newa.append(d)
        book = [newb, newa]
        return book
    elif (exchange == exc.BINANCE):
        bids = book['bids']
        asks = book['asks']
        newb = list()
        for b in bids:
            (p, v, _) = b
            d = {'price': p, 'quantity': v}
            newb.append(d)
        newa = list()
        for a in asks:
            (p, v, _) = a
            d = {'price': p, 'quantity': v}
            newa.append(d)
        book = [newb, newa]
        return book
    elif (exchange == exc.BITMEX):
        asks = list(filter((lambda x: (x['side'] == 'Sell')), book))
        bids = list(filter((lambda x: (x['side'] == 'Buy')), book))
        newb = list()
        for b in bids:
            (p, v) = (float(b['price']), float(b['size']))
            d = {'price': p, 'quantity': v}
            newb.append(d)
        newa = list()
        for a in asks:
            (p, v) = (float(a['price']), float(a['size']))
            d = {'price': p, 'quantity': v}
            newa.append(d)
        newa.reverse()
        dt = datetime.datetime.utcnow()
        dts = dt.strftime('%Y%m%d-%H:%M:%S')
        d = {'bids': newb, 'asks': newa, 'symbol': book[0]['symbol'], 'timestamp': dts}
        return d
    elif (exchange == exc.DERIBIT):
        bids = book['bids']
        asks = book['asks']
        newb = list()
        for b in bids:
            (p, v) = (b['price'], b['quantity'])
            d = {'price': p, 'quantity': v}
            newb.append(d)
        newa = list()
        for a in asks:
            (p, v) = (a['price'], a['quantity'])
            d = {'price': p, 'quantity': v}
            newa.append(d)
        d = {'bids': newb, 'asks': newa}
        return d
