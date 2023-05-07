import numpy as np
import scipy
import sys
import os
import glob
import torch
from scipy.misc import imresize
from PIL import Image
import matplotlib.pyplot as plt
from carla08.agent import CommandFollower
from carla08.client import VehicleControl
from network import CoILModel
from configs import g_conf
from logger import coil_logger
from carla08 import carla_server_pb2 as carla_protocol
import carla


def __init__(self, checkpoint, town_name, carla_version='0.84'):
    self._carla_version = carla_version
    self.checkpoint = checkpoint
    self._model = CoILModel(g_conf.MODEL_TYPE, g_conf.MODEL_CONFIGURATION)
    self.first_iter = True
    self._model.load_state_dict(checkpoint['state_dict'])
    self._model.cuda()
    self._model.eval()
    self.latest_image = None
    self.latest_image_tensor = None
    if (g_conf.USE_ORACLE or g_conf.USE_FULL_ORACLE):
        self.control_agent = CommandFollower(town_name)
