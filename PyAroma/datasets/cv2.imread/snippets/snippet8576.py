import argparse
from lib.loader import VOCSegGroupLoader, VOCSegLoader
from lib.utils import *
from lib.models import *
import pydensecrf.densecrf as dcrf


def run_infer(args, pid=(- 1)):
    data_slice = None
    if (pid >= 0):
        gpus = args.gpus.split(',')
        data_slice = slice(pid, None, len(gpus))
        args.gpus = gpus[pid]
    args.batch_size = len(args.gpus.split(','))
    mod = build_model(args, False)
    loader = VOCSegLoader(args.image_root, None, args.data_list, args.batch_size, args.image_size, pad=True, shuffle=False, rand_scale=False, rand_mirror=False, rand_crop=False, data_slice=data_slice)
    pred_root = args.snapshot
    for (n_batch, batch) in enumerate(loader, 1):
        image_src_list = loader.cache_image_src_list
        mod.forward(batch, is_train=False)
        probs = mod.get_outputs()[0].asnumpy()
        if (not args.no_mirror):
            batch2 = mx.io.DataBatch(data=[batch.data[0][(:, :, :, ::(- 1))]])
            mod.forward(batch2, is_train=False)
            probs_mirror = mod.get_outputs()[0].asnumpy()[(:, :, :, ::(- 1))]
            probs = ((probs + probs_mirror) / 2)
        for (img_src, prob) in zip(image_src_list, probs):
            img = cv2.imread(img_src)[(..., ::(- 1))].copy()
            (h, w) = img.shape[:2]
            prob = prob[(:, :h, :w)]
            pred = prob.argmax(axis=0).astype(np.uint8)
            d = dcrf.DenseCRF2D(w, h, prob.shape[0])
            u = (- prob.reshape(prob.shape[0], (- 1)))
            d.setUnaryEnergy(u)
            d.addPairwiseGaussian(sxy=3, compat=3)
            d.addPairwiseBilateral(sxy=80, srgb=13, rgbim=img, compat=10)
            prob_crf = d.inference(5)
            prob_crf = np.array(prob_crf).reshape((- 1), h, w)
            pred_crf = prob_crf.argmax(axis=0).astype(np.uint8)
            name = os.path.basename(img_src).rsplit('.', 1)[0]
            imwrite(os.path.join(pred_root, 'pred', (name + '.png')), pred)
            imwrite(os.path.join(pred_root, 'pred_crf', (name + '.png')), pred_crf)
