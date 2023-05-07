import lxml.objectify as lxml_objectify
import numpy as np
import pandas as pd


def rollup_option_underlying(options):
    grouped = options.groupby('underlyingSymbol')
    return pd.DataFrame({'mtmYTD': grouped.mtmYTD.sum(), 'realSTYTD': grouped.realSTYTD.sum(), 'realLTYTD': grouped.realLTYTD.sum()})
