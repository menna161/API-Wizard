import argparse
import json
import matplotlib.pyplot as plt
import numpy as np
import torch
from colour import Color
from mdp.plane_obstacles_mdp import PlanarObstaclesMDP
from pc3_model import PC3
from PIL import Image, ImageDraw


def show_latent_map(model, mdp):
    true_map = get_true_map(mdp)
    latent_map = draw_latent_map(model, mdp)
    latent_map = (np.array(latent_map) / 255.0)
    (f, axarr) = plt.subplots(1, 2, figsize=(15, 15))
    axarr[0].imshow(true_map)
    axarr[1].imshow(latent_map)
    plt.show()
