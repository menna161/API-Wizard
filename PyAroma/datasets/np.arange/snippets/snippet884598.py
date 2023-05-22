import glob
import math
import os
import random
import shutil
import time
from pathlib import Path
from threading import Thread
import cv2
import numpy as np
import torch
from PIL import Image, ExifTags
from torch.utils.data import Dataset
from tqdm import tqdm
from utils.utils import xyxy2xywh, xywh2xyxy
from skimage import io


def __init__(self, path, img_size=416, batch_size=16, augment=False, hyp=None, rect=False, image_weights=False, cache_labels=False, cache_images=False, single_cls=False):
    path = str(Path(path))
    assert os.path.isfile(path), ('File not found %s. See %s' % (path, help_url))
    with open(path, 'r') as f:
        self.img_files = [x.replace('/', os.sep) for x in f.read().splitlines() if (os.path.splitext(x)[(- 1)].lower() in img_formats)]
    n = len(self.img_files)
    assert (n > 0), ('No images found in %s. See %s' % (path, help_url))
    bi = np.floor((np.arange(n) / batch_size)).astype(np.int)
    nb = (bi[(- 1)] + 1)
    self.n = n
    self.batch = bi
    self.img_size = img_size
    self.augment = augment
    self.hyp = hyp
    self.image_weights = image_weights
    self.rect = (False if image_weights else rect)
    self.label_files = [x.replace('images', 'labels').replace(os.path.splitext(x)[(- 1)], '.txt') for x in self.img_files]
    if self.rect:
        sp = path.replace('.txt', '.shapes')
        try:
            with open(sp, 'r') as f:
                s = [x.split() for x in f.read().splitlines()]
                assert (len(s) == n), 'Shapefile out of sync'
        except:
            s = [exif_size(Image.open(f)) for f in tqdm(self.img_files, desc='Reading image shapes')]
            np.savetxt(sp, s, fmt='%g')
        s = np.array(s, dtype=np.float64)
        ar = (s[(:, 1)] / s[(:, 0)])
        i = ar.argsort()
        self.img_files = [self.img_files[i] for i in i]
        self.label_files = [self.label_files[i] for i in i]
        self.shapes = s[i]
        ar = ar[i]
        shapes = ([[1, 1]] * nb)
        for i in range(nb):
            ari = ar[(bi == i)]
            (mini, maxi) = (ari.min(), ari.max())
            if (maxi < 1):
                shapes[i] = [maxi, 1]
            elif (mini > 1):
                shapes[i] = [1, (1 / mini)]
        self.batch_shapes = (np.ceil(((np.array(shapes) * img_size) / 32.0)).astype(np.int) * 32)
    self.imgs = ([None] * n)
    self.labels = ([None] * n)
    if (cache_labels or image_weights):
        self.labels = ([np.zeros((0, 5))] * n)
        extract_bounding_boxes = False
        create_datasubset = False
        pbar = tqdm(self.label_files, desc='Caching labels')
        (nm, nf, ne, ns, nd) = (0, 0, 0, 0, 0)
        for (i, file) in enumerate(pbar):
            try:
                with open(file, 'r') as f:
                    l = np.array([x.split() for x in f.read().splitlines()], dtype=np.float32)
            except:
                nm += 1
                continue
            if l.shape[0]:
                assert (l.shape[1] == 5), ('> 5 label columns: %s' % file)
                assert (l >= 0).all(), ('negative labels: %s' % file)
                assert (l[(:, 1:)] <= 1).all(), ('non-normalized or out of bounds coordinate labels: %s' % file)
                if (np.unique(l, axis=0).shape[0] < l.shape[0]):
                    nd += 1
                if single_cls:
                    l[(:, 0)] = 0
                self.labels[i] = l
                nf += 1
                if (create_datasubset and (ns < 10000.0)):
                    if (ns == 0):
                        create_folder(path='./datasubset')
                        os.makedirs('./datasubset/images')
                    exclude_classes = 43
                    if (exclude_classes not in l[(:, 0)]):
                        ns += 1
                        with open('./datasubset/images.txt', 'a') as f:
                            f.write((self.img_files[i] + '\n'))
                if extract_bounding_boxes:
                    p = Path(self.img_files[i])
                    img = cv2.imread(str(p))
                    (h, w) = img.shape[:2]
                    for (j, x) in enumerate(l):
                        f = ('%s%sclassifier%s%g_%g_%s' % (p.parent.parent, os.sep, os.sep, x[0], j, p.name))
                        if (not os.path.exists(Path(f).parent)):
                            os.makedirs(Path(f).parent)
                        b = (x[1:] * [w, h, w, h])
                        b[2:] = b[2:].max()
                        b[2:] = ((b[2:] * 1.3) + 30)
                        b = xywh2xyxy(b.reshape((- 1), 4)).ravel().astype(np.int)
                        b[[0, 2]] = np.clip(b[[0, 2]], 0, w)
                        b[[1, 3]] = np.clip(b[[1, 3]], 0, h)
                        assert cv2.imwrite(f, img[(b[1]:b[3], b[0]:b[2])]), 'Failure extracting classifier boxes'
            else:
                ne += 1
            pbar.desc = ('Caching labels (%g found, %g missing, %g empty, %g duplicate, for %g images)' % (nf, nm, ne, nd, n))
        assert (nf > 0), ('No labels found. See %s' % help_url)
    if cache_images:
        gb = 0
        pbar = tqdm(range(len(self.img_files)), desc='Caching images')
        (self.img_hw0, self.img_hw) = (([None] * n), ([None] * n))
        for i in pbar:
            (self.imgs[i], self.img_hw0[i], self.img_hw[i]) = load_image(self, i)
            gb += self.imgs[i].nbytes
            pbar.desc = ('Caching images (%.1fGB)' % (gb / 1000000000.0))
    detect_corrupted_images = False
    if detect_corrupted_images:
        from skimage import io
        for file in tqdm(self.img_files, desc='Detecting corrupted images'):
            try:
                _ = io.imread(file)
            except:
                print(('Corrupted image detected: %s' % file))
