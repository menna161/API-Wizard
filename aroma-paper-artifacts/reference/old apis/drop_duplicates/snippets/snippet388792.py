from util import *


def cal1(label, vec):
    vec = load_h5(f'{vec}.h5')
    vec = to_dict(vec)
    ret = []
    label = label.drop_duplicates()
    for row in tqdm(label.itertuples()):
        qid = row[1]
        recent_qid = row[2]
        s = cal_cos(qid, recent_qid, vec)
        ret.append((qid, recent_qid, s))
    ret = pd.DataFrame(ret)
    return ret
