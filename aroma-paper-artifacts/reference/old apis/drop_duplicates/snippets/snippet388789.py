from util import *


def dump_user_ques_cos(user_emb_key, ques_emb, index):
    name = f'cos_{user_emb_key}.h5'
    if feature_exists(name):
        return None
    user_emb = load_h5(f'{user_emb_key}.h5')
    user_emb.columns = ['key', 'key_emb']
    user_emb = user_emb.set_index('key').to_dict()['key_emb']
    label_end_day = get_label_end_day(index)
    data = load_data()
    label = data[((data['day'] > get_feature_end_day(label_end_day)) & (data['day'] <= label_end_day))][['uid', 'qid']]
    label = label[['uid', 'qid']].drop_duplicates()
    df = cal_sim(user_emb, ques_emb, label)
    col_key = f'cos_{user_emb_key}'[:(- 2)]
    df.columns = ['uid', 'qid', col_key]
    logger.info('cos null rate %s', (df[col_key].isnull().sum() / len(label)))
    dump_h5(df, name)
    logger.info('dump file %s', name)
