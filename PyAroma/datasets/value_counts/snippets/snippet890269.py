import re
import string
from fastai.text import *
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from ...helpers.training import set_seed


def preds_for_cell_content(test_df, probs, group_by=['cell_content']):
    test_df = test_df.copy()
    test_df['pred'] = np.argmax(probs, axis=1)
    grouped_preds = test_df.groupby(group_by)['pred'].agg((lambda x: x.value_counts().index[0]))
    grouped_counts = test_df.groupby(group_by)['pred'].count()
    results = pd.DataFrame({'true': test_df.groupby(group_by)['label'].agg((lambda x: x.value_counts().index[0])), 'pred': grouped_preds, 'counts': grouped_counts})
    return results
