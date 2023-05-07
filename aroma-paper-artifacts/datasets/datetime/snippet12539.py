from encoder.data_objects.speaker_verification_dataset import SpeakerVerificationDataset
from datetime import datetime
from time import perf_counter as timer
import matplotlib.pyplot as plt
import numpy as np
import visdom
import umap
from encoder import params_data
from encoder import params_model


def __init__(self, env_name=None, update_every=10, server='http://localhost', disabled=False):
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
    self.loss_win = None
    self.eer_win = None
    self.implementation_win = None
    self.projection_win = None
    self.implementation_string = ''
