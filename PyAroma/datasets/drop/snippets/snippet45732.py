import os
import csv
import shutil
import pandas
import numpy as np
from datetime import datetime
from process_mimic_db.utils import *


def build_procedures_table(data_dir, out_dir, conn):
    print('Build procedures_table')
    left = pandas.read_csv(os.path.join(data_dir, 'PROCEDURES_ICD.csv'), dtype=str)
    right = pandas.read_csv(os.path.join(data_dir, 'D_ICD_PROCEDURES.csv'), dtype=str)
    left = left.drop(columns=['ROW_ID', 'SEQ_NUM'])
    right = right.drop(columns=['ROW_ID'])
    out = pandas.merge(left, right, on='ICD9_CODE')
    out = out.sort_values(by='HADM_ID')
    print('-- write table')
    out.to_csv(os.path.join(out_dir, 'PROCEDURES.csv'), sep=',', index=False)
    print('-- write sql')
    out.to_sql('PROCEDURES', conn, if_exists='replace', index=False)
