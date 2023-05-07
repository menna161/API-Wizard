import os
import csv
import shutil
import pandas
import numpy as np
from datetime import datetime
from process_mimic_db.utils import *


def build_lab_table(data_dir, out_dir, conn):
    print('Build lab_table')
    cnt = 0
    show_progress(cnt, 4)
    left = pandas.read_csv(os.path.join(data_dir, 'LABEVENTS.csv'), dtype=str)
    cnt += 1
    show_progress(cnt, 4)
    right = pandas.read_csv(os.path.join(data_dir, 'D_LABITEMS.csv'), dtype=str)
    cnt += 1
    show_progress(cnt, 4)
    left = left.dropna(subset=['HADM_ID', 'VALUE', 'VALUEUOM'])
    left = left.drop(columns=['ROW_ID', 'VALUENUM'])
    left['VALUE_UNIT'] = left[['VALUE', 'VALUEUOM']].apply((lambda x: ''.join(x)), axis=1)
    left = left.drop(columns=['VALUE', 'VALUEUOM'])
    right = right.drop(columns=['ROW_ID', 'LOINC_CODE'])
    cnt += 1
    show_progress(cnt, 4)
    out = pandas.merge(left, right, on='ITEMID')
    cnt += 1
    show_progress(cnt, 4)
    print()
    print('-- write table')
    out.to_csv(os.path.join(out_dir, 'LAB.csv'), sep=',', index=False)
    print('-- write sql')
    out.to_sql('LAB', conn, if_exists='replace', index=False)
