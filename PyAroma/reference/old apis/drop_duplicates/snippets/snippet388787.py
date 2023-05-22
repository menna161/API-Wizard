from util import *


def cal_uid_ans_ques(param):
    (index, col_name) = param
    end_day = get_label_end_day(index)
    data = load_data()
    data = data[((data['day'] > get_feature_end_day(end_day)) & (data['day'] <= end_day))][['uid', 'qid']].drop_duplicates()
    for pooling in get_pooling():
        user_ans_df = load_h5(f'uid_{col_name}_{pooling}_{index}.h5')
        if (col_name == 'ans_t1'):
            ques_df = load_h5(f'qid_title_t1_{pooling}.h5')
        elif (col_name == 'ans_t2'):
            ques_df = load_h5(f'qid_title_t2_{pooling}.h5')
        ques_df.columns = ['key', 'key_emb']
        ques_df = ques_df.set_index('key').to_dict()['key_emb']
        user_ans_df.columns = ['key', 'key_emb']
        user_ans_df = user_ans_df.set_index('key').to_dict()['key_emb']
        df = cal_sim(user_ans_df, ques_df, data)
        dump_h5(df, f'cos_{col_name}_{pooling}_{index}.h5')
