import argparse
from core.model.vgg import vgg16_cam
from core.utils import *
from core.data.VOC import ClassLoader
import multiprocessing as mp
from subprocess import call


def _greedy_merge_superpixels(name, feat_dir, sp_dir, save_dir, num):
    sp = cv2.imread(os.path.join(sp_dir, (name + '.png'))).astype(np.int32)
    sp = ((sp[(..., 0)] + (sp[(..., 1)] * 256)) + (sp[(..., 2)] * 65536))
    (h, w) = sp.shape
    sp_onehot = np.zeros(((sp.max() + 1), (h * w)), np.int32)
    sp_onehot[(sp.ravel(), np.arange((h * w)))] = 1
    sp_size = sp_onehot.sum(axis=1)
    feature = np.load(os.path.join(feat_dir, (name + '.npy')))
    func_sim_feature = (lambda i, j: (feature[i].dot(feature[j]) / (np.linalg.norm(feature[i]) * np.linalg.norm(feature[j]))))
    func_sim_size = (lambda i, j: (1.0 - ((sp_size[i] + sp_size[j]) / (h * w))))
    compute_sim = (lambda i, j: (func_sim_feature(i, j) + func_sim_size(i, j)))
    sp_index = sp_onehot.max(axis=1)
    sim_matrix = np.zeros((sp_index.size, sp_index.size), np.float32)
    for i in range(sp_index.size):
        sim_matrix[(i, i)] = (- np.inf)
        for j in range((i + 1), sp_index.size):
            sim_matrix[(i, j)] = compute_sim(i, j)
            sim_matrix[(j, i)] = sim_matrix[(i, j)]
    while (sp_index.sum() > num):
        (i, j) = np.unravel_index(sim_matrix.argmax(), sim_matrix.shape)
        if (j < i):
            (i, j) = (j, i)
        sp_onehot[i] = np.maximum(sp_onehot[i], sp_onehot[j])
        sp_onehot[(j, :)] = 0
        feature[i] = ((feature[i] * (sp_size[i] / (sp_size[i] + sp_size[j]))) + (feature[j] * (sp_size[j] / (sp_size[i] + sp_size[j]))))
        sp_size[i] = (sp_size[i] + sp_size[j])
        sp_index = sp_onehot.max(axis=1)
        for k in range(sp_index.size):
            sim_matrix[(j, k)] = (- np.inf)
            sim_matrix[(k, j)] = (- np.inf)
            if ((sp_index[k] > 0) and (k != i)):
                sim_matrix[(i, k)] = compute_sim(i, k)
                sim_matrix[(k, i)] = sim_matrix[(i, k)]
    merge_sp = sp_onehot.argmax(axis=0)
    merge_sp = recalibrate_superpixel_index(merge_sp)
    sp_8uc3 = np.array([merge_sp, np.zeros_like(merge_sp), np.zeros_like(merge_sp)])
    sp_8uc3 = sp_8uc3.astype(np.uint8).T.reshape(h, w, 3)
    cv2.imwrite(os.path.join(save_dir, (name + '.png')), sp_8uc3)
