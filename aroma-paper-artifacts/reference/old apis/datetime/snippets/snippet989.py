import os
import json
import datetime
import pandas as pd
import numpy as np
import time
import sys
from src.tool import utc2str, str2list
from src.CHN_prov import CHN_PROV_CODE, CHN_PROV_NAME


def update_df(df, dict_stru):
    '\n    func:\n        update dictionary as structure in dataframe\n    version 1 - stru - 20200124:\n        [total_comfirmed, new_confirmed, modified_timestamp, time_difference]\n    '
    df_last_col = df.columns[(- 1)]
    curr_ts_str = utc2str(time.gmtime())
    df[curr_ts_str] = None
    df_curr_col = df.columns[(- 1)]
    old_total_confirm = str2list(df.loc[(0, [df_last_col])].values[0])[0]
    old_total_dead = str2list(df.loc[(0, [df_last_col])].values[0])[(0 + 2)]
    if (old_total_dead == None):
        old_total_dead = 0
    old_total_cured = str2list(df.loc[(0, [df_last_col])].values[0])[((0 + 2) + 2)]
    if (old_total_cured == None):
        old_total_cured = 0
    old_total_ts = str2list(df.loc[(0, [df_last_col])].values[0])[(2 + 4)]
    new_total_confirm = 0
    new_total_dead = 0
    new_total_cured = 0
    new_total_ts = 0
    for dict_i in dict_stru:
        dict_i_id = int(dict_i['provinceId'])
        if (dict_i_id in CHN_PROV_CODE):
            if (df.loc[(dict_i_id, [df_last_col])].values and (df.loc[(dict_i_id, [df_last_col])].values[0] is not np.nan)):
                old_data_list_str = df.loc[(dict_i_id, [df_last_col])].values[0]
                old_data_list = str2list(old_data_list_str)
                old_confirmed = old_data_list[0]
                old_dead = old_data_list[(0 + 2)]
                if (old_dead == None):
                    old_dead = 0
                old_cured = old_data_list[((0 + 2) + 2)]
                if (old_cured == None):
                    old_cured = 0
                old_ts = old_data_list[(2 + 4)]
                curr_confirmed = dict_i['confirmedCount']
                new_total_confirm += curr_confirmed
                curr_dead = dict_i['deadCount']
                curr_dead_new = (curr_dead - old_dead)
                new_total_dead += curr_dead
                if (curr_dead == 0):
                    curr_dead = None
                    curr_dead_new = None
                curr_cured = dict_i['curedCount']
                curr_cured_new = (curr_cured - old_cured)
                new_total_cured += curr_cured
                if ((curr_cured == 0) and (curr_cured_new == 0)):
                    curr_cured = None
                    curr_cured_new = None
                curr_confirmed_new = (curr_confirmed - old_confirmed)
                curr_ts = (dict_i['modifyTime'] / 1000)
                if (curr_ts > new_total_ts):
                    new_total_ts = curr_ts
                curr_ts_diff = int((((datetime.datetime.utcfromtimestamp(curr_ts) - datetime.datetime.utcfromtimestamp(old_ts)).seconds / 60) / 60))
                update_data_list = [curr_confirmed, curr_confirmed_new, curr_dead, curr_dead_new, curr_cured, curr_cured_new, curr_ts, curr_ts_diff]
            else:
                curr_confirmed = dict_i['confirmedCount']
                curr_ts = (dict_i['modifyTime'] / 1000)
                update_data_list = [curr_confirmed, 0, curr_ts, 0]
            df.loc[(dict_i_id, [df_curr_col])] = [update_data_list]
        elif (dict_i_id == 999):
            if ((dict_i['confirmedCount'] != 0) or (dict_i['suspectedCount'] != 0) or (dict_i['deadCount'] != 0) or (dict_i['curedCount'] != 0)):
                print('[warning] un-determined area in China, total confirmed: {}, total suspected: {}, total dead: {}, total cured: {}'.format(dict_i['confirmedCount'], dict_i['suspectedCount'], dict_i['deadCount'], dict_i['curedCount']))
        else:
            print('[error] prov_code: {} is not in CHN_PROV_CODE'.format(dict_i_id))
    curr_total_diff = int((((datetime.datetime.utcfromtimestamp(new_total_ts) - datetime.datetime.utcfromtimestamp(old_total_ts)).seconds / 60) / 60))
    update_total_list = [new_total_confirm, (new_total_confirm - old_total_confirm), new_total_dead, (new_total_dead - old_total_dead), new_total_cured, (new_total_cured - old_total_cured), new_total_ts, curr_total_diff]
    df.loc[(0, [df_curr_col])] = [update_total_list]
    return df
