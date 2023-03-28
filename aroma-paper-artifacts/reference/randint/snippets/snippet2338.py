import numpy as np
from PIL import Image
import torch
from torch.utils.data import Dataset
from lib.binvox_rw import read_as_3d_array
from lib.config import cfg
from lib.data_augmentation import preprocess_img
from lib.data_io import category_model_id_pair, get_voxel_file, get_rendering_file


def __call__(self, batch):
    '\n        Args:\n            batch (list): a list of samples returned by Dataset.\n        Return:\n            batch (list): Used for training.\n        '
    batch_size = len(batch)
    img_h = cfg.CONST.IMG_W
    img_w = cfg.CONST.IMG_H
    n_vox = cfg.CONST.N_VOX
    n_views = cfg.CONST.N_VIEWS
    if cfg.TRAIN.RANDOM_NUM_VIEWS:
        curr_n_views = (np.random.randint(n_views) + 1)
    else:
        curr_n_views = n_views
    batch_img = np.zeros((curr_n_views, batch_size, 3, img_h, img_w))
    batch_voxel = np.zeros((batch_size, 2, n_vox, n_vox, n_vox))
    for (batch_id, sample) in enumerate(batch):
        (category, model_id) = sample
        image_ids = np.random.choice(cfg.TRAIN.NUM_RENDERING, curr_n_views)
        for (view_id, image_id) in enumerate(image_ids):
            im = self.load_img(category, model_id, image_id)
            batch_img[view_id, batch_id, :, :, :] = im.transpose((2, 0, 1))
        voxel = self.load_label(category, model_id)
        voxel_data = voxel.data
        batch_voxel[batch_id, 0, :, :, :] = (voxel_data < 1)
        batch_voxel[batch_id, 1, :, :, :] = voxel_data
    batch_img = torch.from_numpy(batch_img.astype(np.float32))
    batch_voxel = torch.from_numpy(batch_voxel.astype(np.float32))
    return (batch_img, batch_voxel)
