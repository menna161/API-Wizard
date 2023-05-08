import sys
import time
import theano
import numpy as np
import traceback
from PIL import Image
from six.moves import queue
from multiprocessing import Process, Event
from lib.config import cfg
from lib.data_augmentation import preprocess_img
from lib.data_io import get_voxel_file, get_rendering_file
from lib.binvox_rw import read_as_3d_array
from multiprocessing import Queue
from lib.config import cfg
from lib.data_io import category_model_id_pair


@print_error
def run(self):
    img_h = cfg.CONST.IMG_W
    img_w = cfg.CONST.IMG_H
    n_vox = cfg.CONST.N_VOX
    n_views = cfg.CONST.N_VIEWS
    while ((not self.exit.is_set()) and (self.cur <= self.num_data)):
        db_inds = self.get_next_minibatch()
        if cfg.TRAIN.RANDOM_NUM_VIEWS:
            curr_n_views = (np.random.randint(n_views) + 1)
        else:
            curr_n_views = n_views
        batch_img = np.zeros((curr_n_views, self.batch_size, 3, img_h, img_w), dtype=theano.config.floatX)
        batch_voxel = np.zeros((self.batch_size, n_vox, 2, n_vox, n_vox), dtype=theano.config.floatX)
        for (batch_id, db_ind) in enumerate(db_inds):
            (category, model_id) = self.data_paths[db_ind]
            image_ids = np.random.choice(cfg.TRAIN.NUM_RENDERING, curr_n_views)
            for (view_id, image_id) in enumerate(image_ids):
                im = self.load_img(category, model_id, image_id)
                batch_img[view_id, batch_id, :, :, :] = im.transpose((2, 0, 1)).astype(theano.config.floatX)
            voxel = self.load_label(category, model_id)
            voxel_data = voxel.data
            batch_voxel[batch_id, :, 0, :, :] = (voxel_data < 1)
            batch_voxel[batch_id, :, 1, :, :] = voxel_data
        self.data_queue.put((batch_img, batch_voxel), block=True)
    print('Exiting')
