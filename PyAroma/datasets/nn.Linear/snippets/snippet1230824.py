import torch
from torch import nn, Tensor
from typing import Union, Tuple, List, Iterable, Dict
from ..SentenceTransformer import SentenceTransformer
import logging


def __init__(self, model: SentenceTransformer, sentence_embedding_dimension: int, num_labels: int, concatenation_sent_rep: bool=True, concatenation_sent_difference: bool=True, concatenation_sent_multiplication: bool=False):
    super(SoftmaxLoss, self).__init__()
    self.model = model
    self.num_labels = num_labels
    self.concatenation_sent_rep = concatenation_sent_rep
    self.concatenation_sent_difference = concatenation_sent_difference
    self.concatenation_sent_multiplication = concatenation_sent_multiplication
    num_vectors_concatenated = 0
    if concatenation_sent_rep:
        num_vectors_concatenated += 2
    if concatenation_sent_difference:
        num_vectors_concatenated += 1
    if concatenation_sent_multiplication:
        num_vectors_concatenated += 1
    logging.info('Softmax loss: #Vectors concatenated: {}'.format(num_vectors_concatenated))
    self.classifier = nn.Linear((num_vectors_concatenated * sentence_embedding_dimension), num_labels)
