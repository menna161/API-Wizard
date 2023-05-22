import re
import string
from fastai.text import *
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from ...helpers.training import set_seed


def get_mismatched(self, df, true_label, predicted_label):
    if (self.experiment.merge_fragments and (self.experiment.merge_type != 'concat')):
        print('warning: the returned results are before merging')
    true_label = true_label.value
    predicted_label = predicted_label.value
    probs = self.predict_proba(df['text'])
    preds = np.argmax(probs, axis=1)
    true_y = df['label']
    mismatched_indices = ((true_y == true_label) & (preds == predicted_label))
    mismatched = df[mismatched_indices]
    diff = (probs[(mismatched_indices, true_label)] - probs[(mismatched_indices, predicted_label)])
    indices = diff.argsort()
    mismatched = mismatched.iloc[indices]
    mismatched['pr_diff'] = diff[indices]
    return mismatched
