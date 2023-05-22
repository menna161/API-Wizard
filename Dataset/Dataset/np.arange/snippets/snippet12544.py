from encoder.data_objects.speaker_verification_dataset import SpeakerVerificationDataset
from datetime import datetime
from time import perf_counter as timer
import matplotlib.pyplot as plt
import numpy as np
import visdom
import umap
from encoder import params_data
from encoder import params_model


def draw_projections(self, embeds, utterances_per_speaker, step, out_fpath=None, max_speakers=10):
    max_speakers = min(max_speakers, len(colormap))
    embeds = embeds[:(max_speakers * utterances_per_speaker)]
    n_speakers = (len(embeds) // utterances_per_speaker)
    ground_truth = np.repeat(np.arange(n_speakers), utterances_per_speaker)
    colors = [colormap[i] for i in ground_truth]
    reducer = umap.UMAP()
    projected = reducer.fit_transform(embeds)
    plt.scatter(projected[(:, 0)], projected[(:, 1)], c=colors)
    plt.gca().set_aspect('equal', 'datalim')
    plt.title(('UMAP projection (step %d)' % step))
    if (not self.disabled):
        self.projection_win = self.vis.matplot(plt, win=self.projection_win)
    if (out_fpath is not None):
        plt.savefig(out_fpath)
    plt.clf()
