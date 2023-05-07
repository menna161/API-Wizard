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


def get_objects(colors, materials):
    objects = []
    n_objects = np.random.randint(2, 3)
    for obj_id in range(n_objects):
        side_rand = rand(0, 1)
        size = rand(0.2, 0.4)
        while True:
            cat_id = np.random.randint(55)
            if ((cat_id % 5) != 0):
                break
        shape = random_shape_net(cat_id, True)
        pos_z = (SHAPE_DIMENSIONS[shape][2] * size)
        scale = repeat_scale(size)
        orn_z = rand((- 180), 180)
        if (side_rand < 0.4):
            init_pos = (rand((- 2.5), 0.5), rand((- 4), (- 2)), pos_z)
            init_v = (rand((- 0.6), 0.6), rand(0.5, 1.5), 0)
        elif (side_rand < 0.8):
            init_pos = (rand((- 2.5), 0.5), rand(2, 4), pos_z)
            init_v = (rand((- 0.6), 0.6), rand((- 1.5), (- 0.5)), 0)
        else:
            init_pos = (rand((- 1.5), 0), rand((- 0.8), 0.8), pos_z)
            init_v = (rand((- 0.6), 0.6), rand((- 1.5), 1.5), 0)
        color = colors.pop()
        backward_rand = rand(0, 1)
        if (backward_rand < 0.4):
            backward_time = np.random.randint(200, 300)
            material = materials.pop()
            mid_pos = get_prospective_location(init_pos, init_v, (backward_time / 100))
            object_orginal = dict(shape=shape, color=color, material=material, init_pos=init_pos, init_orn=(0, 0, orn_z), scale=scale, init_v=init_v, disappear_time=backward_time)
            object_stop = dict(shape=shape, color=color, material=material, init_pos=mid_pos, init_orn=(0, 0, orn_z), scale=scale, init_v=[0, 0, 0], appear_time=backward_time, disappear_time=(backward_time + 50))
            object_backward = dict(shape=shape, color=color, material=material, init_pos=mid_pos, init_orn=(0, 0, orn_z), scale=scale, init_v=[(- x) for x in init_v], appear_time=(backward_time + 50))
            for o in [object_orginal, object_stop, object_backward]:
                objects.append(o)
            continue
        object = dict(shape=shape, color=color, material=materials.pop(), init_pos=init_pos, init_orn=(0, 0, orn_z), scale=scale, init_v=init_v)
        objects.append(object)
    return objects
