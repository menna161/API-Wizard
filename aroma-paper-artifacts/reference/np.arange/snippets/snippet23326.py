import torch
import torch.nn as nn
from torch.utils.data.dataset import Dataset
from sentence_transformers import SentenceTransformer
import pandas as pd
import numpy as np
from itertools import combinations
from numpy.linalg import norm
from PIL import Image


def return_adj_matrix(dataframe):
    classes = sorted(dataframe.processed_classes.unique())
    classes_dict = {v: k for (k, v) in enumerate(classes)}
    class_combinations = list(combinations(np.arange(0, len(classes)), r=2))
    sent_bert = SentenceTransformer('bert-base-nli-mean-tokens').eval()
    sentence_embeddings = sent_bert.encode(classes)
    adj_matrix = np.zeros((len(sentence_embeddings), len(sentence_embeddings)))
    normalised_sentence_embeddings = [(i / norm(i)) for i in sentence_embeddings]
    for class_tuple in class_combinations:
        (u, v) = (class_tuple[0], class_tuple[1])
        adj_matrix[class_tuple] = adj_matrix[(v, u)] = (1 - sum((normalised_sentence_embeddings[u] * normalised_sentence_embeddings[v])))
    return adj_matrix
