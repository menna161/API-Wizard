import os
import json
import sys
from io import BytesIO
import argparse
import numpy as np
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from scipy.cluster import hierarchy
from scipy.spatial.distance import squareform, pdist
import task_similarity
import glob
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns


def main():
    os.makedirs('./plots', exist_ok=True)
    files = glob.glob(os.path.join(args.root, '*', 'embedding.p'))
    embeddings = [task_similarity.load_embedding(file) for file in files]
    embeddings.sort(key=(lambda x: x.meta['dataset']['task_id']))
    for e in embeddings:
        e.task_id = e.meta['dataset']['task_id']
        e.task_name = e.meta['task_name']
        e.dataset = (CUB if (e.task_id < CUB_NUM_TASKS) else INAT)
    distance_matrix = task_similarity.pdist(embeddings, distance=args.distance)
    add_class_information(embeddings)
    for e in embeddings:
        assert hasattr(e, 'task_name')
        assert ('class' in e.meta), e.task_name
        assert hasattr(e, 'dataset'), e.task_name
    names = [(f"[{e.dataset}] {e.task_name} ({e.meta['class']})" if ('order' in e.meta) else f"[{e.dataset}] {e.task_name} ({e.meta['class']})") for e in embeddings]
    embeddings = np.array(embeddings)
    tax_distance_matrix = np.zeros_like(distance_matrix)
    for (i, e0) in enumerate(embeddings):
        for (j, e1) in enumerate(embeddings):
            tax_distance_matrix[(i, j)] = taxonomy_distance(e0, e1)
    sns.set_style('whitegrid')
    plt.close('all')
    sns.set_style('whitegrid')
    fig = plt.figure(figsize=(3.3, 3.3))
    ax = fig.gca()
    np.fill_diagonal(distance_matrix, np.inf)
    np.fill_diagonal(tax_distance_matrix, np.inf)
    plot_changing_k(ax, distance_matrix, embeddings, embeddings, label='Task2Vec distance')
    plot_changing_k(ax, tax_distance_matrix, embeddings, embeddings, label='Taxonomy distance')
    np.fill_diagonal(distance_matrix, 0)
    np.fill_diagonal(tax_distance_matrix, 0)
    ax.legend()
    fig.savefig('plots/embedding_distace_vs_taxonomy.pdf', bbox_inches='tight')
    np.fill_diagonal(distance_matrix, 0.0)
    embeddings = embeddings[:50]
    names = names[:50]
    distance_matrix = distance_matrix[(:50, :50)]
    (distance_matrix, embeddings, names, _) = sort_distance_matrix(distance_matrix, embeddings, names, method='complete')
    plt.close('all')
    sns.set_style('white')
    draw_figure_to_plt(distance_matrix, embeddings, names, label_size=22)
    plt.savefig('plots/task2vec_distance_matrix.pdf', format=args.format, dpi=None, bbox_inches='tight')
