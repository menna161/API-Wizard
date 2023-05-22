from encoder.data_objects import SpeakerVerificationDataLoader, SpeakerVerificationDataset
from encoder.params_model import *
from encoder.model import SpeakerEncoder
from pathlib import Path
import torch
from encoder.data_objects.speaker_verification_dataset import SpeakerVerificationDataset
from datetime import datetime
from time import perf_counter as timer
import matplotlib.pyplot as plt
import numpy as np
import visdom
import umap
import seaborn as sns
import pandas as pd


def draw_projections(self, embeds, utterances_per_speaker, step, name, out_fpath=None, max_speakers=10):
    max_speakers = min(max_speakers, len(colormap))
    embeds = embeds[:(max_speakers * utterances_per_speaker)]
    sex = [s.split('/')[(- 1)].split('_')[(- 1)] for s in name]
    sex = sex[:max_speakers]
    res_sex = []
    for s in sex:
        for i in range(10):
            res_sex.append(s)
    n_speakers = (len(embeds) // utterances_per_speaker)
    ground_truth = np.repeat(np.arange(n_speakers), utterances_per_speaker)
    colors = [colormap[i] for i in ground_truth]
    markers = [marker[s] for s in res_sex]
    reducer = umap.UMAP()
    projected = reducer.fit_transform(embeds)
    sns.scatterplot(projected[(:, 0)], projected[(:, 1)], hue=ground_truth, style=markers)
    plt.gca().set_aspect('equal', 'datalim')
    plt.title(('UMAP projection (step %d)' % step))
    if (not self.disabled):
        self.projection_win = self.vis.matplot(plt, win=self.projection_win)
    if (out_fpath is not None):
        plt.savefig(out_fpath)
    plt.clf()
