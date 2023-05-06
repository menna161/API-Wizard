from util import *
import argparse
import gc


def cal_1(label, key='uid', diff_key='diff_day_inv_ques'):
    t = label[[key, diff_key]].copy()
    t['flag'] = 1
    a = t.groupby([key, diff_key])['flag'].sum().reset_index()
    a.columns = [key, diff_key, 'each_count']
    b = t.groupby(key)[diff_key].nunique().reset_index()
    b.columns = [key, 'diff_day_nunq']
    a = pd.merge(a, b, on=key, how='left')
    a['choose'] = np.where((a['each_count'] > 1), 1, 0)
    a['key'] = (a.groupby(key)['choose'].transform('sum') / a['diff_day_nunq'])
    a = a[[key, 'key']].drop_duplicates(key)
    return a
