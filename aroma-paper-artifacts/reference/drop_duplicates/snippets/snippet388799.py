from util import *


def process1(index):
    data = load_data()
    ques_emb = load_h5('qid_topic_mean.h5')
    ques_emb = to_dict(ques_emb)
    user_inter_emb = load_h5('uid_inter_topic_mean.h5')
    user_inter_emb = to_dict(user_inter_emb)
    user_follow_emb = load_h5('uid_follow_topic_mean.h5')
    user_follow_emb = to_dict(user_follow_emb)
    label_end_day = get_label_end_day(index)
    label = data[((data['day'] > get_feature_end_day(label_end_day)) & (data['day'] <= label_end_day))][['uid', 'qid']]
    label = label[['uid', 'qid']].drop_duplicates()
    print(label.shape)
    filename = f'user_follow_topic_emb_cos_{index}.h5'
    if (not feature_exists(filename, False)):
        df = cal_sim(user_follow_emb, ques_emb, label)
        dump_h5(df, filename)
    filename = f'user_inter_topic_emb_cos_{index}.h5'
    if (not feature_exists(filename, False)):
        df = cal_sim(user_inter_emb, ques_emb, label)
        dump_h5(df, filename)
