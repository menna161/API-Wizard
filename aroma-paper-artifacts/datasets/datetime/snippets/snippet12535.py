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


def finalize(self):
    self.write_line('Statistics:')
    for (param_name, values) in self.sample_data.items():
        self.write_line(('\t%s:' % param_name))
        self.write_line(('\t\tmin %.3f, max %.3f' % (np.min(values), np.max(values))))
        self.write_line(('\t\tmean %.3f, median %.3f' % (np.mean(values), np.median(values))))
    self.write_line('-----')
    end_time = str(datetime.now().strftime('%A %d %B %Y at %H:%M'))
    self.write_line(('Finished on %s' % end_time))
    self.text_file.close()
