import numpy as np
import scipy.sparse as sp
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from .vectorizer import LogEntropyVectorizer, BM25Vectorizer
from sklearn.decomposition import PCA, TruncatedSVD
from sklearn.neighbors import NearestNeighbors
from sklearn.metrics.pairwise import euclidean_distances, cosine_distances


def compute_topics(papers: list, weighting='tfidf', projection='svd', min_df=3, max_df=0.8, lowercase=True, norm='l2', analyzer='word', token_pattern='\\w{1,}', ngram_range=(1, 1), n_components=30, stop_words='english'):
    '\n    Compute topics from a given list of ``papers``\n    '
    if (weighting == 'count'):
        model = CountVectorizer(min_df=min_df, max_df=max_df, token_pattern=token_pattern, ngram_range=ngram_range, stop_words=stop_words)
    elif (weighting == 'tfidf'):
        model = TfidfVectorizer(min_df=min_df, max_df=max_df, lowercase=lowercase, norm=norm, token_pattern=token_pattern, ngram_range=ngram_range, use_idf=True, smooth_idf=True, sublinear_tf=True, stop_words=stop_words)
    elif (weighting == 'entropy'):
        model = LogEntropyVectorizer(min_df=min_df, max_df=max_df, lowercase=lowercase, token_pattern=token_pattern, ngram_range=ngram_range, stop_words=stop_words)
    elif (weighting == 'bm25'):
        model = BM25Vectorizer(min_df=min_df, max_df=max_df, lowercase=lowercase, token_pattern=token_pattern, ngram_range=ngram_range, stop_words=stop_words)
    else:
        print("select weighting scheme from ['count', 'tfidf', 'entropy', 'bm25']")
    X = model.fit_transform(papers)
    if (projection == 'svd'):
        topic_model = TruncatedSVD(n_components=n_components, algorithm='arpack')
        X_topic = topic_model.fit_transform(X)
    elif (projection == 'pca'):
        topic_model = PCA(n_components=n_components)
        X_topic = topic_model.fit_transform(X.todense())
    else:
        print("select projection from ['svd', 'pca']")
    return X_topic
