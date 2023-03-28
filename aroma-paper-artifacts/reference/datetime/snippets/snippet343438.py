from archon.exchange.deribit.Wrapper import DeribitWrapper
import archon.config as config
from datetime import datetime


def get_options_expiring_soon(opts):
    print('** options expring in next 20 days ** ')
    for x in opts:
        exp = x['expiration']
        n = datetime.now()
        dt = datetime.strptime(exp, '%Y-%m-%d %H:%M:%S GMT')
        expiry_from = (dt - n)
        if (expiry_from.days < 40):
            try:
                s = x['strike']
                ot = x['optionType']
                inst = x['instrumentName']
                summary = w.getsummary(inst)
                ask = float(summary['askPrice'])
                bid = float(summary['bidPrice'])
                spread = ((ask - bid) / ask)
                print(s, ot, exp, summary['last'], spread)
            except:
                continue
