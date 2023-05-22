import re
import string
from fastai.text import *
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from ...helpers.training import set_seed


def test_model(model, tdf):
    probs = model(tdf['text'])
    preds = np.argmax(probs, axis=1)
    print('Results of categorisation on text fagment level')
    print(metrics(preds, tdf.label))
    print('Results per cell_content grouped using majority voting')
    results = preds_for_cell_content(tdf, probs)
    print(metrics(results['pred'], results['true']))
    print('Results per cell_content grouped with multi category mean')
    results = preds_for_cell_content_multi(tdf, probs)
    print(metrics(results['pred'], results['true']))
    print('Results per cell_content grouped with multi category mean - only on fragments from the same paper that the coresponding table')
    results = preds_for_cell_content_multi(tdf[tdf.this_paper], probs[tdf.this_paper])
    print(metrics(results['pred'], results['true']))
