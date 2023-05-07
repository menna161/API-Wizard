import os
import csv
import shutil
import pandas
import numpy as np
from datetime import datetime
from process_mimic_db.utils import *


def build_prescriptions_table(data_dir, out_dir, conn):
    print('Build prescriptions_table')
    data = pandas.read_csv(os.path.join(data_dir, 'PRESCRIPTIONS.csv'), dtype=str)
    data = data.drop(columns=['ROW_ID', 'GSN', 'DRUG_NAME_POE', 'DRUG_NAME_GENERIC', 'NDC', 'PROD_STRENGTH', 'FORM_VAL_DISP', 'FORM_UNIT_DISP', 'STARTDATE', 'ENDDATE'])
    data = data.dropna(subset=['DOSE_VAL_RX', 'DOSE_UNIT_RX'])
    data['DRUG_DOSE'] = data[['DOSE_VAL_RX', 'DOSE_UNIT_RX']].apply((lambda x: ''.join(x)), axis=1)
    data = data.drop(columns=['DOSE_VAL_RX', 'DOSE_UNIT_RX'])
    print('-- write table')
    data.to_csv(os.path.join(out_dir, 'PRESCRIPTIONS.csv'), sep=',', index=False)
    print('-- write sql')
    data.to_sql('PRESCRIPTIONS', conn, if_exists='replace', index=False)
