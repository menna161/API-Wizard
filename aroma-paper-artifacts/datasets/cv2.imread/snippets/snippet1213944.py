import argparse
from core.model.vgg import vgg16_cam
from core.utils import *
from core.data.VOC import ClassLoader
import multiprocessing as mp
from subprocess import call


def _extract_superpixel_features(name, image_dir, sp_dir, dense_feat_dir, sp_feat_dir, infer_size, delete_dense_feature=False, gpu=None):
    image = cv2.imread(os.path.join(image_dir, (name + '.jpg')))
    (h, w) = image.shape[:2]
    sp = cv2.imread(os.path.join(sp_dir, (name + '.png'))).astype(np.int32)
    sp = ((sp[(..., 0)] + (sp[(..., 1)] * 256)) + (sp[(..., 2)] * 65536))
    assert (sp.shape == (h, w)), (name, image.shape, sp.shape)
    context = (mx.cpu() if (gpu is None) else mx.gpu(gpu))
    feature = np.load(os.path.join(dense_feat_dir, (name + '.npy')))
    feature = mx.nd.array(feature[np.newaxis], ctx=context)
    feature = mx.nd.contrib.BilinearResize2D(feature, height=infer_size, width=infer_size)
    feature = feature[(0, :, :h, :w)].reshape((- 1), (h * w))
    sp = mx.nd.one_hot(mx.nd.array(sp, ctx=context), depth=(sp.max() + 1)).reshape((h * w), (- 1))
    sp_feature = mx.nd.dot(sp, feature, transpose_a=True, transpose_b=True)
    sp_feature /= mx.nd.maximum(sp.sum(axis=0, keepdims=True).T, 1e-05)
    sp_feature = sp_feature.asnumpy()
    np.save(os.path.join(sp_feat_dir, (name + '.npy')), sp_feature)
    if delete_dense_feature:
        call(['rm', os.path.join(dense_feat_dir, (name + '.npy'))])
