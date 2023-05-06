from util import *


def flatten_qid_topic(target):
    ret = []
    df = target[['qid', 'topic']].drop_duplicates(['qid'])
    for row in tqdm(df.itertuples()):
        kid = row[1]
        topic = row[2]
        for t in topic:
            ret.append((kid, t))
    df = pd.DataFrame.from_records(ret)
    df.columns = ['qid', 'topic']
    return df
