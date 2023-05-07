import csv
import json
import os
import math
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import pearsonr, spearmanr, kendalltau
import torch
from pytorch_pretrained_bert import GPT2Tokenizer, GPT2LMHeadModel
from pytorch_pretrained_bert import BertTokenizer, BertForMaskedLM
from configuration import CONFIG_DIR
from experiments_output import OUTPUT_DIR


def visualize_correlation_metrics(spearman_scores, kendall_scores, pearson_scores, model_name, year):
    '\n    Visualize the scores of correlation metrics with respect to k-worst bpes you tried\n    :param spearman_scores: The spearman correlation scores of Q1 and k-worst bpes each time\n    :param kendall_scores: The Kendall correlation scores of Q1 and k-worst bpes each time\n    :param pearson_scores: The Pearson correlation scores of Q1 and k-worst bpes each time\n    :param model_name: Name of Language Model you used (BERT or GPT2). It is used on the output file name\n    :param year: The corresponding year of the data\n    '
    x_ticks = [i for i in range(1, (MAX_BPES_TO_SEARCH + 1))]
    plt.figure(figsize=(26, 8))
    y_max = max(spearman_scores)
    x_pos = spearman_scores.index(y_max)
    x_max = x_ticks[x_pos]
    plt.subplot(1, 3, 1)
    plt.plot(x_ticks, spearman_scores, 'bo')
    plt.annotate('{0:.2f} K={1:d}'.format(y_max, x_max), xy=(x_max, y_max), xytext=(x_max, (y_max + 0.005)))
    plt.title('Spearman')
    plt.xlabel('# of worst words')
    y_max = max(kendall_scores)
    x_pos = kendall_scores.index(y_max)
    x_max = x_ticks[x_pos]
    plt.subplot(1, 3, 2)
    plt.plot(x_ticks, kendall_scores, 'bo')
    plt.annotate('{0:.2f} K={1:d}'.format(y_max, x_max), xy=(x_max, y_max), xytext=(x_max, (y_max + 0.005)))
    plt.title('Kendall')
    plt.xlabel('# of worst words')
    y_max = max(pearson_scores)
    x_pos = pearson_scores.index(y_max)
    x_max = x_ticks[x_pos]
    plt.subplot(1, 3, 3)
    plt.plot(x_ticks, pearson_scores, 'bo')
    plt.annotate('{0:.2f} K={1:d}'.format(y_max, x_max), xy=(x_max, x_max), xytext=(x_max, (y_max + 0.005)))
    plt.title('Pearson')
    plt.xlabel('# of worst words')
    path_to_save = os.path.join(OUTPUT_DIR, 'Q1 - {0:s}  {1:s}.png'.format(model_name, year))
    plt.savefig(path_to_save)
    plt.show()
