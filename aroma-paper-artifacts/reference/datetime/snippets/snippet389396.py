import time
import backtrader as bt
import datetime as dt
from ccxtbt import CCXTStore
from config import BINANCE, ENV, PRODUCTION, COIN_TARGET, COIN_REFER, DEBUG
from dataset.dataset import CustomDataset
from sizer.percent import FullMoney
from strategies.basic_rsi import BasicRSI
from utils import print_trade_analysis, print_sqn, send_telegram_message


def main():
    cerebro = bt.Cerebro(quicknotify=True)
    if (ENV == PRODUCTION):
        broker_config = {'apiKey': BINANCE.get('key'), 'secret': BINANCE.get('secret'), 'nonce': (lambda : str(int((time.time() * 1000)))), 'enableRateLimit': True}
        store = CCXTStore(exchange='binance', currency=COIN_REFER, config=broker_config, retries=5, debug=DEBUG)
        broker_mapping = {'order_types': {bt.Order.Market: 'market', bt.Order.Limit: 'limit', bt.Order.Stop: 'stop-loss', bt.Order.StopLimit: 'stop limit'}, 'mappings': {'closed_order': {'key': 'status', 'value': 'closed'}, 'canceled_order': {'key': 'status', 'value': 'canceled'}}}
        broker = store.getbroker(broker_mapping=broker_mapping)
        cerebro.setbroker(broker)
        hist_start_date = (dt.datetime.utcnow() - dt.timedelta(minutes=30000))
        data = store.getdata(dataname=('%s/%s' % (COIN_TARGET, COIN_REFER)), name=('%s%s' % (COIN_TARGET, COIN_REFER)), timeframe=bt.TimeFrame.Minutes, fromdate=hist_start_date, compression=30, ohlcv_limit=99999)
        cerebro.adddata(data)
    else:
        data = CustomDataset(name=COIN_TARGET, dataname='dataset/binance_nov_18_mar_19_btc.csv', timeframe=bt.TimeFrame.Minutes, fromdate=dt.datetime(2018, 9, 20), todate=dt.datetime(2019, 3, 13), nullvalue=0.0)
        cerebro.resampledata(data, timeframe=bt.TimeFrame.Minutes, compression=30)
        broker = cerebro.getbroker()
        broker.setcommission(commission=0.001, name=COIN_TARGET)
        broker.setcash(100000.0)
        cerebro.addsizer(FullMoney)
    cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name='ta')
    cerebro.addanalyzer(bt.analyzers.SQN, _name='sqn')
    cerebro.addstrategy(BasicRSI)
    initial_value = cerebro.broker.getvalue()
    print(('Starting Portfolio Value: %.2f' % initial_value))
    result = cerebro.run()
    final_value = cerebro.broker.getvalue()
    print(('Final Portfolio Value: %.2f' % final_value))
    print(('Profit %.3f%%' % (((final_value - initial_value) / initial_value) * 100)))
    print_trade_analysis(result[0].analyzers.ta.get_analysis())
    print_sqn(result[0].analyzers.sqn.get_analysis())
    if DEBUG:
        cerebro.plot()
