import argparse
import os
import numpy as np
import random
from PIL import Image
import shutil


def rotate(file_list, data_list, name):
    os.makedirs(os.path.join(args.save_path, 'rotate'), exist_ok=True)
    for (i, item) in enumerate(data_list):
        print('[rotate image] processing {0} ...'.format(i))
        x = Image.open(item[0])
        angle = random.randint(0, 360)
        x = x.rotate(angle)
        file_list.append([os.path.join(args.save_path, 'rotate', (((str(i) + '_') + name) + '.jpg')), item[1]])
        x.save(os.path.join(args.save_path, 'rotate', (((str(i) + '_') + name) + '.jpg')))
