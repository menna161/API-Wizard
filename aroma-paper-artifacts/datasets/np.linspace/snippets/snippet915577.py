import bpy
import os
import numpy as np
from PIL import Image
from imageio import imread
from render.camera import set_camera
from utils.geometry import convert_euler


def get_intro_camera(rendering, n):
    nn = int((n / 8))
    phi_s = np.concatenate([np.linspace(rendering.camera_phi, (rendering.camera_phi + 10), nn), np.linspace((rendering.camera_phi + 10), rendering.camera_phi, nn), np.linspace(rendering.camera_phi, (rendering.camera_phi - 10), nn), np.linspace((rendering.camera_phi - 10), rendering.camera_phi, nn), np.linspace(rendering.camera_phi, rendering.camera_phi, (nn * 4))])
    theta_s = np.concatenate([np.linspace(rendering.camera_theta, rendering.camera_theta, (nn * 4)), np.linspace(rendering.camera_theta, (rendering.camera_theta - 10), nn), np.linspace((rendering.camera_theta - 10), rendering.camera_theta, nn), np.linspace(rendering.camera_theta, (rendering.camera_theta + 10), nn), np.linspace((rendering.camera_theta + 10), rendering.camera_theta, nn)])
    return (phi_s, theta_s)
