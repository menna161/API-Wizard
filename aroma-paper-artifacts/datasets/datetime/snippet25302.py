import lxml.objectify as lxml_objectify
import numpy as np
import pandas as pd


def clean_option_perf(perf):
    perf = perf[(perf.assetCategory == 'OPT')].copy()
    perf['expiry'] = pd.to_datetime(perf['expiry'])
    return perf
