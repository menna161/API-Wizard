import numpy as np
import scipy.cluster.hierarchy as sch
from gensim import corpora
from gensim import models
from scipy.stats import entropy


def doc2vec(documents, topics_ratio, passes):
    dictionary = corpora.Dictionary(documents)
    corpus = [dictionary.doc2bow(doc_list) for doc_list in documents]
    ldamodel = models.LdaModel(corpus=corpus, num_topics=int((len(documents) * topics_ratio)), id2word=dictionary, passes=passes)
    lda_vec = np.zeros([len(documents), int((len(documents) * topics_ratio))])
    for (i, doc_bow) in enumerate(corpus):
        topic = [topic_pr[0] for topic_pr in ldamodel[doc_bow]]
        lda_vec[i][topic] = [topic_pr[1] for topic_pr in ldamodel[doc_bow]]
    return lda_vec
