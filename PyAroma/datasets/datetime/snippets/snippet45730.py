import os
import csv
import shutil
import pandas
import numpy as np
from datetime import datetime
from process_mimic_db.utils import *


def build_demographic_table(data_dir, out_dir, conn):
    print('Build demographic_table')
    pat_id2name = get_patient_name('process_mimic_db')
    pat_info = read_table(data_dir, 'PATIENTS.csv')
    adm_info = read_table(data_dir, 'ADMISSIONS.csv')
    print('-- Process PATIENTS')
    cnt = 0
    for itm in pat_info:
        cnt += 1
        show_progress(cnt, len(pat_info))
        itm['NAME'] = pat_id2name[itm['SUBJECT_ID']]
        dob = datetime.strptime(itm['DOB'], '%Y-%m-%d %H:%M:%S')
        itm['DOB_YEAR'] = str(dob.year)
        if (len(itm['DOD']) > 0):
            dod = datetime.strptime(itm['DOD'], '%Y-%m-%d %H:%M:%S')
            itm['DOD_YEAR'] = str(dod.year)
        else:
            itm['DOD_YEAR'] = ''
    pat_dic = {ky['SUBJECT_ID']: ky for ky in pat_info}
    print()
    print('-- Process ADMISSIONS')
    cnt = 0
    for itm in adm_info:
        cnt += 1
        show_progress(cnt, len(adm_info))
        for ss in pat_dic[itm['SUBJECT_ID']]:
            if ((ss == 'ROW_ID') or (ss == 'SUBJECT_ID')):
                continue
            itm[ss] = pat_dic[itm['SUBJECT_ID']][ss]
        admtime = datetime.strptime(itm['ADMITTIME'], '%Y-%m-%d %H:%M:%S')
        itm['ADMITYEAR'] = str(admtime.year)
        dctime = datetime.strptime(itm['DISCHTIME'], '%Y-%m-%d %H:%M:%S')
        itm['DAYS_STAY'] = str((dctime - admtime).days)
        itm['AGE'] = str((int(itm['ADMITYEAR']) - int(itm['DOB_YEAR'])))
        if (int(itm['AGE']) > 89):
            itm['AGE'] = str(((89 + int(itm['AGE'])) - 300))
    print()
    print('-- write table')
    header = ['SUBJECT_ID', 'HADM_ID', 'NAME', 'MARITAL_STATUS', 'AGE', 'DOB', 'GENDER', 'LANGUAGE', 'RELIGION', 'ADMISSION_TYPE', 'DAYS_STAY', 'INSURANCE', 'ETHNICITY', 'EXPIRE_FLAG', 'ADMISSION_LOCATION', 'DISCHARGE_LOCATION', 'DIAGNOSIS', 'DOD', 'DOB_YEAR', 'DOD_YEAR', 'ADMITTIME', 'DISCHTIME', 'ADMITYEAR']
    fout = open(os.path.join(out_dir, 'DEMOGRAPHIC.csv'), 'w')
    fout.write((('"' + '","'.join(header)) + '"\n'))
    for itm in adm_info:
        arr = []
        for wd in header:
            arr.append(itm[wd])
        fout.write((('"' + '","'.join(arr)) + '"\n'))
    fout.close()
    print('-- write sql')
    data = pandas.read_csv(os.path.join(out_dir, 'DEMOGRAPHIC.csv'), dtype={'HADM_ID': str, 'DOD_YEAR': float, 'SUBJECT_ID': str})
    data.to_sql('DEMOGRAPHIC', conn, if_exists='replace', index=False)
