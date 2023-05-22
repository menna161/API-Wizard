import re
import numpy as np
import pandas as pd
from ...helpers.training import set_seed
from ... import config
from .type_predictor import TableTypePredictor, TableType
from .structure_predictor import TableStructurePredictor


def normalize(self, df):
    df = df.drop_duplicates(['text', 'cell_content', 'cell_type']).fillna('')
    df = df.replace(re.compile('(xxref|xxanchor)-[\\w\\d-]*'), '\\1 ')
    df = df.replace(re.compile('(^|[ ])\\d+\\.\\d+\\b'), ' xxnum ')
    df = df.replace(re.compile('(^|[ ])\\d\\b'), ' xxnum ')
    df = df.replace(re.compile('\\bdata set\\b'), ' dataset ')
    return df
