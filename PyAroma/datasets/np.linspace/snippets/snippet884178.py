import time
import numpy as np
import pickle
import vispy
import math
import time
import threading
import qtpy.QtWidgets
from vispy import gloo, app


def set_new_node_positions(self, new_positions, new_weights=None, new_focus=None):
    old_num_nodes = self.node_positions.shape[1]
    num_nodes = new_positions.shape[1]
    with self.lock:
        self.node_positions = new_positions
        self._node_positions_px = new_positions.copy()
        if (num_nodes != old_num_nodes):
            self.num_nodes = self.node_positions.shape[1]
            self.nodes_program['depth'] = np.linspace(0.0, 1.0, num=self.num_nodes).astype(np.float32)
        if ((new_weights is None) and (num_nodes != old_num_nodes)):
            self.node_weights = np.ones((self.num_frames, num_nodes), dtype=np.float32)
        elif (new_weights is not None):
            self.node_weights = new_weights
        if ((new_focus is None) and (num_nodes != old_num_nodes)):
            self.focus = (np.zeros(num_nodes) > 0.0)
        elif (new_focus is not None):
            self.focus = new_focus
