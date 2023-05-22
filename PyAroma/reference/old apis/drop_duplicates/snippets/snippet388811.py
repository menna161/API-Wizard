from util import *


def merge_ans_feature(target, feature_end):
    '\n    :param target: label\n    :param ans: ans\n    :param feature_end:\n    :return:\n    '
    feature = ans[(ans['a_day'] <= feature_end)].copy()
    feature['ans'] = 1
    target = merge_lag(target, feature, 'uid', 'a_day', sub='ans')
    target = merge_lag(target, feature, 'qid', 'a_day', sub='ans')
    target = get_diff_day(target, feature, dt_col='a_day', sub='ans')
    key = 'hour'
    target = get_merge_feature(target, feature, key, 'ans', ['count'])
    key = 'weekday'
    target = get_merge_feature(target, feature, key, 'ans', ['count'])
    key = 'weekday_hour'
    target = get_merge_feature(target, feature, key, 'ans', ['count'])
    target['weekday_hour_uid'] = make_key(target['weekday_hour'], target['uid'])
    feature['weekday_hour_uid'] = make_key(feature['weekday_hour'], feature['uid'])
    target = get_merge_feature(target, feature, 'weekday_hour_uid', 'ans', ['count'])
    del target['weekday_hour_uid']
    target['hour_uid'] = make_key(target['hour'], target['uid'])
    feature['hour_uid'] = make_key(feature['hour'], feature['uid'])
    target = get_merge_feature(target, feature, 'hour_uid', 'ans', ['count'])
    del target['hour_uid']
    target['weekday_uid'] = make_key(target['weekday'], target['uid'])
    feature['weekday_uid'] = make_key(feature['weekday'], feature['uid'])
    target = get_merge_feature(target, feature, 'weekday_uid', 'ans', ['count'])
    del target['weekday_uid']
    key = 'uid'
    target = get_merge_feature(target, feature, key, 'ans', ['count'])
    target = get_merge_feature(target, feature, key, 'ans_t1_count', ['mean', 'sum', 'max', 'std'])
    target = get_merge_feature(target, feature, key, 'ans_t2_count', ['mean', 'sum', 'max', 'std'])
    target = get_merge_feature(target, feature, key, 'has_img', ['mean', 'sum'])
    target = get_merge_feature(target, feature, key, 'word_count', ['mean', 'sum', 'max'])
    target = get_merge_feature(target, feature, key, 'reci_cheer', ['mean', 'sum', 'max', 'std'])
    target = get_merge_feature(target, feature, key, 'reci_mark', ['mean', 'sum', 'max', 'std'])
    target = get_merge_feature(target, feature, key, 'diff_day_ques_ans', ['mean', 'sum', 'max', 'std'])
    target = get_merge_feature(target, feature, key, 'reci_tks', ['mean', 'sum'])
    target = get_merge_feature(target, feature, key, 'reci_uncheer', ['mean', 'sum'])
    target = get_merge_feature(target, feature, key, 'reci_comment', ['mean', 'sum', 'max', 'std'])
    feature_win = feature[(feature['a_day'] >= (feature_end - 2))]
    target = get_merge_feature(target, feature_win, key, 'reci_cheer', ['mean', 'sum'], sub=2)
    feature_win = feature[(feature['a_day'] >= (feature_end - 2))]
    target = get_merge_feature(target, feature_win, key, 'reci_comment', ['mean', 'sum'], sub=2)
    feature_win = feature[(feature['a_day'] >= (feature_end - 2))]
    target = get_merge_feature(target, feature_win, key, 'word_count', ['mean', 'sum', 'max'], sub=1)
    feature_win = feature[(feature['a_day'] >= (feature_end - 2))]
    target = get_merge_feature(target, feature_win, key, 'word_count', ['mean', 'sum', 'max'], sub=2)
    key = 'qid'
    target = get_merge_feature(target, feature, key, 'ans', ['count'])
    target = get_merge_feature(target, feature, key, 'ans_t2_count', ['mean', 'sum', 'max', 'std'])
    target = get_merge_feature(target, feature, key, 'has_img', ['mean'])
    target = get_merge_feature(target, feature, key, 'word_count', ['mean', 'sum', 'max'])
    target = get_merge_feature(target, feature, key, 'diff_day_ques_ans', ['mean', 'std', 'sum', 'max'])
    target = get_merge_feature(target, feature, key, 'reci_tks', ['mean'])
    target = get_merge_feature(target, feature, key, 'reci_mark', ['mean'])
    target = get_merge_feature(target, feature, key, 'reci_comment', ['mean', 'sum'])
    target = get_merge_feature(target, feature, key, 'reci_cheer', ['mean', 'sum'])
    target = get_merge_feature(target, feature, key, 'reci_uncheer', ['mean'])
    feature_win = feature[(feature['a_day'] >= (feature_end - 1))]
    target = get_merge_feature(target, feature_win, key, 'word_count', ['mean', 'sum', 'max'], sub=1)
    feature_win = feature[(feature['a_day'] >= (feature_end - 2))]
    target = get_merge_feature(target, feature_win, key, 'word_count', ['mean', 'sum', 'max'], sub=2)
    feature = feature[['uid', 'qid', 'a_day', 'reci_cheer', 'reci_tks', 'word_count']]
    t = feature.groupby(['uid', 'a_day'])[('reci_cheer', 'reci_tks', 'word_count')].max().reset_index()
    t = t.sort_values(['uid', 'a_day'])
    for col in ['a_day', 'word_count', 'reci_cheer', 'reci_tks']:
        t[f'lag_{col}'] = t[col].shift(1)
        t.loc[((t['uid'] != t['uid'].shift(1)), f'lag_{col}')] = None
    t = t.drop_duplicates(['uid'], keep='last')
    target = merge_dict(target, t, 'uid')
    target = cal_ans_lag_feature(target)
    return target
