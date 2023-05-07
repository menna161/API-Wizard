import argparse
from core.data.VOC import SuperpixelLoader
from core.utils import *
from core.model.vgg import *
from core.model.layers_custom import *
import multiprocessing as mp
import pydensecrf.densecrf as dcrf


def _generate_seed(name, cam_root, icd_root, img_root, ann_root, sal_root, save_root, infer_size, num_cls, confidence):
    label = VOC.get_annotation(os.path.join(ann_root, (name + '.xml')))
    image = cv2.imread(os.path.join(img_root, (name + '.jpg')))
    (h, w) = image.shape[:2]
    scores = np.load(os.path.join(icd_root, (name + '.npy')))
    scores = np.array([cv2.resize(x, (infer_size, infer_size))[(:h, :w)] for x in scores])
    scores_fg = (np.maximum(scores, 0) / np.maximum(scores.max(axis=(1, 2), keepdims=True), 1e-05))
    proposal_fg = (scores_fg > 1e-05)
    candidate_fg = proposal_fg.argmax(axis=0)
    if (len(label) > 1):
        cams = np.load(os.path.join(cam_root, (name + '.npy')))
        cams = np.array([cv2.resize(x, (infer_size, infer_size))[(:h, :w)] for x in cams])
        comp_scores = (norm_score(np.maximum(cams, 0)) * scores_fg)
        conflict_fg = (proposal_fg.sum(axis=0) > 1)
        candidate_fg = ((candidate_fg * (1 - conflict_fg)) + (comp_scores.argmax(axis=0) * conflict_fg))
    fg = proposal_fg.max(axis=0)
    if (sal_root is not None):
        sal_src = os.path.join(sal_root, (name + '.png'))
        assert os.path.exists(sal_src), sal_src
        sal = (cv2.imread(sal_src, 0).astype(np.float32) / 255)
        bg = (sal < 0.01)
        if ((1.0 - (float(bg.sum()) / bg.size)) < 0.01):
            scores_bg = (np.minimum(scores, 0) / np.minimum(scores.min(axis=(1, 2), keepdims=True), (- 1e-05)))
            bg &= (scores_bg > 1e-05).min(axis=0)
    else:
        scores_bg = (np.minimum(scores, 0) / np.minimum(scores.min(axis=(1, 2), keepdims=True), (- 1e-05)))
        bg = (scores_bg > 1e-05).min(axis=0)
    undefined = (~ (bg ^ fg))
    if (len(label) > 1):
        undefined |= (((comp_scores.max(axis=0) - comp_scores.min(axis=0)) <= 1e-05) & fg)
    seed = (np.array(label) + 1)[candidate_fg.ravel()].reshape(h, w).astype(np.uint8)
    seed[bg] = 0
    seed[undefined] = 255
    if (sal_root is not None):
        imwrite(os.path.join(save_root, 'sal', (name + '.png')), seed)
    else:
        seed_prob = confidence
        res_prob = ((1 - seed_prob) / num_cls)
        prob = np.full((256, (h * w)), res_prob, np.float32)
        prob[(seed.ravel(), np.arange((h * w)))] = seed_prob
        prob = prob[:num_cls]
        prob /= prob.sum(axis=0, keepdims=True)
        u = (- np.log(np.maximum(prob, 1e-05)))
        d = dcrf.DenseCRF2D(w, h, num_cls)
        d.setUnaryEnergy(u)
        d.addPairwiseGaussian(sxy=3, compat=3)
        d.addPairwiseBilateral(sxy=80, srgb=13, rgbim=image[(..., ::(- 1))].copy(), compat=10)
        prob_crf = d.inference(10)
        prob_crf = np.array(prob_crf).reshape(num_cls, h, w)
        prob_crf /= prob_crf.sum(axis=0, keepdims=True)
        seed_crf = prob_crf.argmax(axis=0).astype(np.uint8)
        seed_crf[(prob_crf.max(axis=0) < 0.1)] = 255
        imwrite(os.path.join(save_root, 'crf', (name + '.png')), seed_crf)
