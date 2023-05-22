import re
import string
from fastai.text import *
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from ...helpers.training import set_seed


def preds_for_cell_content_multi(test_df, probs, group_by=['cell_content']):
    test_df = test_df.copy()
    probs_df = pd.DataFrame(probs, index=test_df.index)
    test_df = pd.concat([test_df, probs_df], axis=1)
    grouped_preds = np.argmax(test_df.groupby(group_by)[probs_df.columns].sum().values, axis=1)
    grouped_counts = test_df.groupby(group_by)['label'].count()
    results = pd.DataFrame({'true': test_df.groupby(group_by)['label'].agg((lambda x: x.value_counts().index[0])), 'pred': grouped_preds, 'counts': grouped_counts})
    return results
