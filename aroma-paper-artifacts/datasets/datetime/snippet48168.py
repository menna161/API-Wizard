import datetime


def parse_transaction_date(transaction) -> datetime.date:
    return datetime.datetime.strptime(transaction['time'][:10], '%Y-%m-%d').date()
