from multiprocessing import Pool, cpu_count
import os
import random
import numpy as np
from easydict import EasyDict
from dataset.make_all import generate
from utils.geometry import random_spherical_point, get_prospective_location
from utils.io import mkdir, write_serialized, catch_abort
from utils.constants import CONFIG_FOLDER, SIM_OUTPUT_FOLDER, RENDER_OUTPUT_FOLDER, VIDEO_OUTPUT_FOLDER, OCCLUDER_HALF_WIDTH
from utils.misc import rand, random_distinct_colors, repeat_scale, get_host_id, BlenderArgumentParser
from utils.shape_net import SHAPE_DIMENSIONS, random_shape_net


def get_occluders(colors, materials):
    occluders = []
    occluder_rand = rand(0, 1)
    init_pos = (rand((- 0.5), 0.5), rand((- 1.0), 1.0), 0)
    half_width = rand(0.5, 1.5)
    half_height = rand(0.5, 1.0)
    scale = (OCCLUDER_HALF_WIDTH, half_width, half_height)
    init_orn = (0, 0, rand((- 20), 20))
    if (occluder_rand < 0.85):
        joint_rand = rand(0, 1)
        joint_t = np.random.randint(10, 25)
        if (joint_rand < (1 / 6)):
            joint_pattern = [(90, 90, joint_t), (90, 0, (250 - joint_t)), (0, 90, (250 - joint_t)), (90, 90, joint_t)]
        elif (joint_rand < (1 / 3)):
            joint_pattern = [(90, 90, joint_t), (90, 0, (250 - joint_t)), (0, (- 90), (250 - joint_t)), ((- 90), (- 90), joint_t)]
        elif (joint_rand < 0.5):
            joint_pattern = [((- 90), (- 90), joint_t), ((- 90), 0, (250 - joint_t)), (0, 90, (250 - joint_t)), (90, 90, joint_t)]
        elif (joint_rand < (2 / 3)):
            joint_pattern = [((- 90), (- 90), joint_t), ((- 90), 0, (250 - joint_t)), (0, (- 90), (250 - joint_t)), ((- 90), (- 90), joint_t)]
        elif (joint_rand < (5 / 6)):
            joint_pattern = [(0, 0, joint_t), (0, 90, (250 - joint_t)), (90, 0, (250 - joint_t)), (0, 0, joint_t)]
        else:
            joint_pattern = [(0, 0, joint_t), (0, (- 90), (250 - joint_t)), ((- 90), 0, (250 - joint_t)), (0, 0, joint_t)]
        occluder = dict(shape='cube', color=colors.pop(), joint='revolute', material=materials.pop(), init_pos=init_pos, init_orn=init_orn, scale=scale, joint_pattern=joint_pattern)
        occluders.append(occluder)
    elif (occluder_rand < 0.9):
        joint_rand = rand(0, 1)
        if (joint_rand < 0.25):
            joint_pattern = [(rand(0.6, 1.2), 0, 250), (0, rand(0.6, 1.2), 250)]
        elif (joint_rand < 0.5):
            joint_pattern = [(rand(0.6, 1.2), 0, 250), (0, rand((- 1.2), (- 0.6)), 250)]
        elif (joint_rand < 0.75):
            joint_pattern = [(rand((- 1.2), (- 0.6)), 0, 250), (0, rand(0.6, 1.2), 250)]
        else:
            joint_pattern = [(rand((- 1.2), (- 0.6)), 0, 250), (0, rand((- 1.2), (- 0.6)), 250)]
        occluder = dict(shape='cube', color=colors.pop(), joint='prismatic', material=materials.pop(), init_pos=init_pos, init_orn=init_orn, scale=scale, joint_pattern=joint_pattern)
        occluders.append(occluder)
    return occluders
