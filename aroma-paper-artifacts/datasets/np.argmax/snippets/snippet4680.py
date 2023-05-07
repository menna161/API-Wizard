from __future__ import division
from tools.model import load_model
from config.configs_kf import *
from lib.utils.visual import *
import torchvision.transforms as st
from sklearn.metrics import confusion_matrix
import numpy as np
from tqdm import tqdm_notebook as tqdm
from tools.ckpt import *
import time
import itertools


def tta_real_test(nets, all=False, labels=land_classes, norm=False, test_set=None, stride=600, batch_size=5, window_size=(512, 512)):
    test_files = loadtestimg(test_set)
    idlist = loadids(test_set)
    all_preds = []
    num_class = len(labels)
    ids = []
    total_ids = 0
    for k in test_set[IDS].keys():
        total_ids += len(test_set[IDS][k])
    for (img, id) in tqdm(zip(test_files, idlist), total=total_ids, leave=False):
        img = np.asarray(img, dtype='float32')
        img = st.ToTensor()(img)
        img = (img / 255.0)
        if norm:
            img = st.Normalize(*mean_std)(img)
        img = img.cpu().numpy().transpose((1, 2, 0))
        stime = time.time()
        with torch.no_grad():
            pred = fusion_prediction(nets, image=img, scales=[1.0], batch_size=batch_size, num_class=num_class, wsize=window_size)
        print('inference cost time: ', (time.time() - stime))
        pred = np.argmax(pred, axis=(- 1))
        for key in ['boundaries', 'masks']:
            pred = (pred * np.array((cv2.imread(os.path.join('/media/liu/diskb/data/Agriculture-Vision/test', key, (id + '.png')), (- 1)) / 255), dtype=int))
        filename = './{}.png'.format(id)
        cv2.imwrite(os.path.join(output_path, filename), pred)
        all_preds.append(pred)
        ids.append(id)
    if all:
        return (all_preds, ids)
    else:
        return all_preds
