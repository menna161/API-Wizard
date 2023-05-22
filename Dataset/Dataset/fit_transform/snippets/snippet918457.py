import numpy as np
import os
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer


def generate_correlation_matrics(input_file_path, output_file_path):
    blogs = []
    with open(os.path.join(MYDIR, input_file_path), 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            content = line.split(',')[2]
            blogs.append(content)
    vectorizer = CountVectorizer()
    count = vectorizer.fit_transform(blogs)
    transformer = TfidfTransformer()
    tfidf = transformer.fit_transform(count)
    weight = tfidf.toarray()
    correlation_matrics = []
    n = len(blogs)
    for i in range(n):
        tmp = []
        for j in range(n):
            cos_between_two_matric = cos_sim(weight[i], weight[j])
            tmp.append(cos_between_two_matric)
        correlation_matrics.append(tmp)
    with open(os.path.join(MYDIR, output_file_path), 'w', encoding='utf-8') as f:
        for i in correlation_matrics:
            content = ' '.join((('%s' % num) for num in i))
            f.write((content + '\n'))
    f.close()
