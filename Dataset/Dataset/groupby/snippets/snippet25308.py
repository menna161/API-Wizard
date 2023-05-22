import lxml.objectify as lxml_objectify
import numpy as np
import pandas as pd


def total_fees(cash_trans):
    total_by_type = cash_trans.groupby('type').amount.sum()
    return total_by_type[['Broker Interest Paid', 'Broker Interest Received', 'Other Fees']]
