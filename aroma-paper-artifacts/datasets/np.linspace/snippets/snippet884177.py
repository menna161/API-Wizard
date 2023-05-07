import time
import numpy as np
import pickle
import vispy
import math
import time
import threading
import qtpy.QtWidgets
from vispy import gloo, app


def __init__(self, node_positions, edge_textures=None, node_weights=None, focus=None, animate=True, translate=True, draw_callback=None, size=(800, 600)):
    super().__init__(size=size, vsync=True)
    resolution = np.array([self.physical_size[0], self.physical_size[1]]).astype(np.float32)
    self._start_shift = np.float32([0, 0])
    self._start_scale = 1.0
    self._start_theta = 0.0
    self._current_shift = np.float32([0, 0])
    self._current_scale = 1.0
    self._current_theta = 0.0
    self._target_shift = np.float32([0, 0])
    self._target_scale = 1.0
    self._target_theta = 0.0
    self._transition_position = 1.0
    self._current_transition_frame = 0
    self._transition_start_point = 0.0
    self.transition_duration = None
    self.loop_duration = 4.0
    self.sync_timepoint = 0.0
    self.min_node_radius = 0.002
    self.node_radius_factor = 0.002
    self.weight_scaling_offset = 0.1
    self.node_alpha_factor = 0.3
    self.num_frames = node_positions.shape[0]
    self.scale_factor = 3.0
    self.num_frames = node_positions.shape[0]
    self.animate = animate
    self.translate = translate
    self.draw_callback = draw_callback
    self.lock = threading.Lock()
    if (edge_textures is None):
        edge_textures = np.zeros([self.num_frames, 2, 2], dtype=np.float32)
    self.edges_program = gloo.Program(edges_vertex_shader, edges_fragment_shader)
    self.edges_colors = np.array([[0.0, 0.0, 0.0, 1.0], [1.0, 1.0, 1.0, 1.0]]).astype(np.float32)
    self.edge_textures = edge_textures
    self.edges_program['texcoord'] = np.float32([[0, 1], [1, 1], [0, 0], [1, 0]])
    self.edges_program['texture'] = gloo.Texture2D(data=self.edge_textures[0], interpolation='linear', format='alpha')
    self.edges_program['position'] = np.float32([[(- 1), 1], [1, 1], [(- 1), (- 1)], [1, (- 1)]])
    self.nodes_program = gloo.Program(nodes_vertex_shader, nodes_fragment_shader)
    self.node_colors = np.array([[1.0, 0.0, 0.0, 1.0], [0.8, 0.8, 0.0, 1.0], [0.0, 1.0, 0.0, 1.0], [0.0, 0.8, 0.8, 1.0], [0.0, 0.0, 1.0, 1.0], [0.8, 0.0, 0.8, 1.0], [1.0, 0.0, 0.0, 1.0]]).astype(np.float32)
    if (node_weights is None):
        node_weights = np.ones((self.num_frames, node_positions.shape[1])).astype(np.float32)
    self.node_weights = node_weights
    self.node_positions = node_positions
    self._node_positions_px = self.node_positions.copy()
    self.num_nodes = self.node_positions.shape[1]
    self.nodes_program['depth'] = np.linspace(0.0, 1.0, num=self.num_nodes).astype(np.float32)
    self.nodes_program['center'] = self.node_positions[0]
    self.nodes_program['alpha'] = (np.zeros(self.num_nodes).astype(np.float32) + 0.5)
    scaling = np.float32([(resolution[0] / max(resolution)), (resolution[1] / max(resolution))])
    self.nodes_program['scaling'] = scaling
    self.focus_program = gloo.Program(focus_vertex_shader, focus_fragment_shader)
    if (focus is None):
        focus = (np.zeros(self.node_positions.shape[1]) > 0.0)
    self.focus = focus
    self.focus_color = np.array([0.5, 1.0, 1.0, 0.5]).astype(np.float32)
    self.focus_program['center'] = self.node_positions[(0, self.focus[0])]
    self.focus_program['radius'] = 0.005
    gloo.set_state(blend=False, clear_color='black')
    gloo.set_viewport(0, 0, self.physical_size[0], self.physical_size[1])
    self._current_frame = 0
