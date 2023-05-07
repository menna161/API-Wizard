from multiprocess.pool import ThreadPool
from encoder.params_data import *
from encoder.config import librispeech_datasets, anglophone_nationalites, data_shell
from datetime import datetime
from encoder import audio
from pathlib import Path
from tqdm import tqdm
import numpy as np
import os
from encoder import params_data


def __init__(self, root, name):
    self.text_file = open(Path(root, ('Log_%s.txt' % name.replace('/', '_'))), 'w')
    self.sample_data = dict()
    start_time = str(datetime.now().strftime('%A %d %B %Y at %H:%M'))
    self.write_line(('Creating dataset %s on %s' % (name, start_time)))
    self.write_line('-----')
    self._log_params()
