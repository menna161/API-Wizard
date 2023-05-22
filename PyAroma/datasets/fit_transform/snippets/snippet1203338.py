import argparse
import os
import string
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import tinynn as tn
from sklearn.manifold import TSNE


def visualize(model, idx2word, args):
    test_x = np.diag(np.ones(len(idx2word)))
    embed_layer = model.net.layers[0]
    embedding = ((test_x @ embed_layer.params['w']) + embed_layer.params['b'])
    labels = list(idx2word.values())
    embedding_reduced = TSNE().fit_transform(embedding)
    plt.figure(figsize=(12, 6))
    words = ['he', 'she', 'man', 'woman', 'is', 'are', 'you', 'i']
    for word in words:
        i = labels.index(word)
        (x, y) = embedding_reduced[i]
        plt.scatter(x, y)
        plt.annotate(labels[i], (x, y))
    if (not os.path.isdir(args.output_dir)):
        os.makedirs(args.output_dir)
    output_path = os.path.join(args.output_dir, 'tsne-sample.jpg')
    plt.savefig(output_path)
    plt.close()
    print(f'visualization result: {output_path}')
