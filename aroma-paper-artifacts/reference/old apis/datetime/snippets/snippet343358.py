import archon.exchange.cryptofacilities as cfApi
import datetime
import time
import archon.config as config
from datetime import datetime


def withdraw():
    targetAddress = 'xxxxxxxxxx'
    currency = 'xbt'
    amount = 0.12345678
    result = cfclient.send_withdrawal(targetAddress, currency, amount)
    print('send_withdrawal:\n', result)
    lastTransferTime = (datetime.datetime.strptime('2016-02-01', '%Y-%m-%d').isoformat() + '.000Z')
    result = cfclient.get_transfers(lastTransferTime=lastTransferTime)
    print('get_transfers:\n', result)
    fromAccount = 'fi_ethusd'
    toAccount = 'cash'
    unit = 'eth'
    amount = 0.1
    result = cfclient.transfer(fromAccount, toAccount, unit, amount)
    print('transfer:\n', result)
