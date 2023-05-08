from util import *


def flatten_uid_qid_topic(target):
    ret = []
    df = target[['uid', 'qid', 'topic']].drop_duplicates(['uid', 'qid'])
    for row in tqdm(df.itertuples()):
        uid = row[1]
        qid = row[2]
        topic = row[3]
        for t in topic:
            ret.append((uid, qid, t))
    df = pd.DataFrame.from_records(ret)
    df.columns = ['uid', 'qid', 'topic']
    return df
