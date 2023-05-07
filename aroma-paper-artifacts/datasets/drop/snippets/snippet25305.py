import lxml.objectify as lxml_objectify
import numpy as np
import pandas as pd


def rollup_statements(statements, key='mtm_ytd'):

    def clean(x):
        return x.drop('Total', axis=1)
    result = clean(getattr(statements[0], key))
    for stmt in statements[1:]:
        result = result.add(clean(getattr(stmt, key)), fill_value=0)
    result = result.fillna(0)
    result['Total'] = result.sum(1)
    return result
