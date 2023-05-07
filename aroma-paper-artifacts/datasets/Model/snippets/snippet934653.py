import glob
import logging
import math
import os
import sys
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import scipy
from scipy.misc import imresize
import torch
from coilutils.drive_utils import checkpoint_parse_configuration_file
from configs import g_conf, merge_with_yaml
from network import CoILModel
from srunner.challenge.autoagents.autonomous_agent import AutonomousAgent, Track
from agents.navigation.local_planner import RoadOption
import carla


def setup(self, path_to_config_file):
    (yaml_conf, checkpoint_number) = checkpoint_parse_configuration_file(path_to_config_file)
    checkpoint = torch.load(os.path.join('/', os.path.join(*os.path.realpath(__file__).split('/')[:(- 2)]), '_logs', yaml_conf.split('/')[(- 2)], yaml_conf.split('/')[(- 1)].split('.')[(- 2)], 'checkpoints', (str(checkpoint_number) + '.pth')))
    merge_with_yaml(os.path.join('/', os.path.join(*os.path.realpath(__file__).split('/')[:(- 2)]), yaml_conf))
    self.checkpoint = checkpoint
    self._model = CoILModel(g_conf.MODEL_TYPE, g_conf.MODEL_CONFIGURATION)
    self.first_iter = True
    logging.info('Setup Model')
    self._model.load_state_dict(checkpoint['state_dict'])
    self._model.cuda()
    self._model.eval()
    self.latest_image = None
    self.latest_image_tensor = None
    self._expand_command_front = 5
    self._expand_command_back = 3
    self.track = Track.CAMERAS
