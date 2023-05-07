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


def __init__(self, env_name=None, update_every=10, server='http://localhost', disabled=True):
    self.last_update_timestamp = timer()
    self.update_every = update_every
    self.step_times = []
    self.losses = []
    self.eers = []
    print(('Updating the visualizations every %d steps.' % update_every))
    self.disabled = disabled
    if self.disabled:
        return
    now = str(datetime.now().strftime('%d-%m %Hh%M'))
    if (env_name is None):
        self.env_name = now
    else:
        self.env_name = ('%s (%s)' % (env_name, now))
    try:
        self.vis = visdom.Visdom(server, env=self.env_name, raise_exceptions=True)
    except ConnectionError:
        raise Exception('No visdom server detected. Run the command "visdom" in your CLI to start it.')
