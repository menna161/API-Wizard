import os
import csv
import shutil
import pandas
import numpy as np
from datetime import datetime
from process_mimic_db.utils import *


def build_diagnoses_table(data_dir, out_dir, conn):
    print('Build diagnoses_table')
    left = pandas.read_csv(os.path.join(data_dir, 'DIAGNOSES_ICD.csv'), dtype=str)
    right = pandas.read_csv(os.path.join(data_dir, 'D_ICD_DIAGNOSES.csv'), dtype=str)
    left = left.drop(columns=['ROW_ID', 'SEQ_NUM'])
    right = right.drop(columns=['ROW_ID'])
    out = pandas.merge(left, right, on='ICD9_CODE')
    out = out.sort_values(by='HADM_ID')
    print('-- write table')
    out.to_csv(os.path.join(out_dir, 'DIAGNOSES.csv'), sep=',', index=False)
    print('-- write sql')
    out.to_sql('DIAGNOSES', conn, if_exists='replace', index=False)
