import os
import os.path
import cv2
import numpy as np
import random
import pickle
from PIL import Image, ImageFile


def get_item(self, frame_index):
    if (self.frame_stride == (- 1)):
        strides = [1, 2, 4]
        frame_stride = strides[random.randint(0, 2)]
        tube_path = os.path.join(self.jta_root, ((((('tubes_' + str(self.forward_frames)) + '_') + str(frame_stride)) + '_') + str(self.min_vis)), self.type, self.video_name)
        self.tube_folder = tube_path
        if ('s3:' in self.tube_folder):
            self.tube_folder = ((self.tube_folder[:3] + '/') + self.tube_folder[3:])
        if (self.type == 'train'):
            assert os.path.exists(os.path.join(self.tube_folder)), ('Tube folder does not exist: ' + str(os.path.join(self.tube_folder)))
    else:
        frame_stride = self.frame_stride
    start_frame = frame_index
    max_len = ((self.forward_frames * 2) * frame_stride)
    tube_file = os.path.join(self.tube_folder, str(start_frame))
    if (self.type == 'train'):
        if (not os.path.exists(tube_file)):
            print(tube_file)
            return (None, None, None, None, None)
    img_meta = {}
    image = self._getimage(frame_index)
    if (image is None):
        print(os.path.join(self.img_folder, 'img1/{}.jpg'.format((frame_index + 1))))
    img_meta['img_shape'] = [max_len, image.shape[0], image.shape[1]]
    img_meta['value_range'] = self.value_range
    img_meta['pad_percent'] = [1, 1]
    img_meta['video_name'] = os.path.basename(self.img_folder)
    img_meta['start_frame'] = start_frame
    imgs = []
    for i in range((self.forward_frames * 2)):
        frame_index = (start_frame + (i * frame_stride))
        image = self._getimage(frame_index)
        imgs.append(image)
    tubes = np.zeros((1, 15))
    if (self.type == 'train'):
        tubes = pickle.load(open(tube_file, 'rb'))
    num_dets = len(tubes)
    labels = np.ones((num_dets, 1))
    tubes = np.array(tubes)
    imgs = np.array(imgs)
    return (imgs, img_meta, tubes, labels, start_frame)
