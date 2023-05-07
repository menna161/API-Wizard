import lxml.objectify as lxml_objectify
import numpy as np
import pandas as pd


def clean_stock_perf(perf):
    perf = perf[(perf.assetCategory == 'STK')]
    perf = perf.drop(['acctAlias', 'assetCategory', 'expiry', 'multiplier', 'putCall', 'strike', 'securityID', 'securityIDType', 'underlyingSymbol', 'underlyingConid'], axis='columns')
    return perf.set_index('symbol')
