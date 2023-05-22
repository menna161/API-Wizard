import json
import math
import random
import itertools
import numpy as np
import pandas as pd
import scipy as sp
import collections
import threading
from scipy.linalg import eigh, cholesky
from scipy.stats import norm
import scipy.interpolate as interpolate
from optparse import OptionParser
import time
import os
from collections import OrderedDict


def normalize(self):
    if ('tables' not in self.sample_json):
        raise Exception('no tables defined in sample json')
    tables = self.sample_json['tables']['dimension']
    table_dfs = {}
    for tbl in tables:
        table_dfs[tbl['name']] = pd.DataFrame(columns=tbl['columns'])
    for (chunk_id, chunk) in enumerate(pd.read_csv(self.options.normalize, chunksize=100000, header=0)):
        all_from_fields = []
        for tbl in tables:
            table_df = table_dfs[tbl['name']]
            for mapping in tbl['mapping']:
                xx = chunk[mapping['fromFields']]
                xx.columns = tbl['columns']
                table_df = table_df.append(xx)
                table_df = table_df.drop_duplicates(subset=tbl['columns'])
            table_df = table_df.reset_index(drop=True)
            table_df.index.name = 'ID'
            table_dfs[tbl['name']] = table_df
            if ('tmp_ID' in table_df.columns):
                del table_df['tmp_ID']
            table_df.to_csv(tbl['name'], index=True, mode='w')
            table_df['tmp_ID'] = table_df.index
            count = 0
            for mapping in tbl['mapping']:
                all_from_fields.extend(mapping['fromFields'])
                boo = len(chunk)
                beforechunk = chunk
                chunk = pd.merge(chunk, table_df, how='left', left_on=mapping['fromFields'], right_on=tbl['columns'])
                chunk = chunk.rename(columns={'tmp_ID': mapping['fk']})
                for c in tbl['columns']:
                    del chunk[c]
        for c in all_from_fields:
            del chunk[c]
        if (chunk_id == 0):
            chunk.to_csv(self.options.output, index=False, mode='w')
        else:
            chunk.to_csv(self.options.output, index=False, header=False, mode='a')
