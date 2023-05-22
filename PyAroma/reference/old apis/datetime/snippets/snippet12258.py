import os
from datetime import datetime
from ..compat import tfv1 as tf
from ..utils import fs, logger
from .base import Callback


def _before_train(self):
    time = datetime.now().strftime('%m%d-%H%M%S')
    self.saver.export_meta_graph(os.path.join(self.checkpoint_dir, 'graph-{}.meta'.format(time)), collection_list=self.graph.get_all_collection_keys())
