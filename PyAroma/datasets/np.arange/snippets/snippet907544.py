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


def draw_figure_to_plt(distance_matrix, embeddings, names, label_size=14):
    fig = plt.figure(figsize=(((15 / 25.0) * len(embeddings)), ((15 / 25.0) * len(embeddings))))
    ax = plt.gca()
    plt.imshow(distance_matrix, cmap='viridis_r')
    ax.set_xticks(np.arange(len(embeddings)))
    ax.set_yticks(np.arange(len(embeddings)))
    ax.set_xticklabels(names)
    ax.set_yticklabels(names)
    plt.setp(ax.get_xticklabels(), rotation=45, ha='right', rotation_mode='anchor')
    try:
        for (i, e) in enumerate(embeddings):
            arr_img = get_image(e)
            imagebox = OffsetImage(arr_img, zoom=0.18)
            imagebox.image.axes = ax
            xy = (i, i)
            ab = AnnotationBbox(imagebox, xy, frameon=False)
            ax.add_artist(ab)
    except FileNotFoundError:
        print('Could not find an icon for a taxonomy entry. Have you downloaded the iconic_taxa directory in ./static?')
    plt.tick_params(axis='both', which='major', labelsize=label_size)
    plt.tight_layout()
