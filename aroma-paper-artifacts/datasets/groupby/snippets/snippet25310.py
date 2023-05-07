import lxml.objectify as lxml_objectify
import numpy as np
import pandas as pd


def __init__(self, path):
    self.path = path
    stmt = self.get_lxml_root()
    self.perf = clean_perf(stmt)
    self.option_perf = clean_option_perf(self.perf)
    self.option_perf_underlying = rollup_option_underlying(self.option_perf)
    self.stock_perf = clean_stock_perf(self.perf)
    self.cash_transactions = clean_cash(stmt)
    self.dividends = clean_dividends(self.cash_transactions)
    dividends_by_symbol = self.dividends.groupby('symbol').amount.sum()
    self.mtm_ytd = pd.DataFrame({'Stocks': self.stock_perf.mtmYTD, 'Options': self.option_perf_underlying.mtmYTD, 'Dividends': dividends_by_symbol}).fillna(0)
    self.realized = pd.DataFrame({'Stocks': self.stock_perf.realSTYTD, 'Options': self.option_perf_underlying.realSTYTD, 'Dividends': dividends_by_symbol}).fillna(0)
    self.mtm_ytd['Total'] = self.mtm_ytd.sum(1)
    self.realized['Total'] = self.realized.sum(1)
    self.cash_by_type = self.cash_transactions.groupby('type').amount.sum()
    self.fees = self.cash_by_type[['Broker Interest Paid', 'Broker Interest Received', 'Other Fees']]
    self.in_out = clean_in_out(self.cash_transactions)
