import re
import string
from fastai.text import *
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from ...helpers.training import set_seed


def transform_df(df):
    df = df.replace(re.compile('(xxref|xxanchor)-[\\w\\d-]*'), '\\1 ')
    df = df.replace(re.compile('(^|[ ])\\d+\\.\\d+\\b'), ' xxnum ')
    df = df.replace(re.compile('(^|[ ])\\d\\b'), ' xxnum ')
    df = df.replace(re.compile('\\bdata set\\b'), ' dataset ')
    df = df.drop_duplicates(['text', 'cell_content', 'cell_type']).fillna('')
    return df
