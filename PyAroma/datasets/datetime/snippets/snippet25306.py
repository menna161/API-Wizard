import lxml.objectify as lxml_objectify
import numpy as np
import pandas as pd


def clean_cash(statement):
    cash_trans = get_table(statement.CashTransactions)
    cash_trans.amount = cash_trans.amount.astype(np.float64)
    cash_trans.dateTime = pd.to_datetime(cash_trans.dateTime)
    return cash_trans
