import argparse
from core.data.VOC import SuperpixelLoader
from core.utils import *
from core.model.vgg import *
from core.model.layers_custom import *
import multiprocessing as mp
import pydensecrf.densecrf as dcrf


def run_infer(args):
    mod = build_model(args, for_training=False)
    loader = SuperpixelLoader(args.image_root, args.annotation_root, args.superpixel_root, args.data_list, args.batch_size, args.image_size, pad_dataset=True, shuffle=False, rand_scale=False, rand_mirror=False, rand_crop=False)
    v_images = [[] for _ in range(args.num_cls)]
    NUM = 20
    for (n_batch, batch) in enumerate(loader, 1):
        mod.forward(batch, is_train=False)
        outputs = [x.asnumpy() for x in mod.get_outputs()]
        (cam, icd_bu, icd_bu_sp, icd_td) = outputs
        image_src_list = loader.cache_image_src_list
        label = batch.label[0].asnumpy()
        (N, C, H, W) = icd_td.shape
        for (img_src, label, cam, icd_bu, icd_bu_sp, icd_td) in zip(image_src_list, label, cam, icd_bu, icd_bu_sp, icd_td):
            Ls = np.nonzero(label)[0]
            cam = cam[Ls]
            icd = icd_td[Ls]
            name = os.path.basename(img_src).rsplit('.', 1)[0]
            npsave(os.path.join(args.snapshot, 'results', 'scores_cam', (name + '.npy')), cam)
            npsave(os.path.join(args.snapshot, 'results', 'scores_icd', (name + '.npy')), icd)
            if (len(Ls) == 1):
                L = Ls[0]
                if (len(v_images[L]) < NUM):
                    image = cv2.imread(img_src)
                    (h, w) = image.shape[:2]
                    getScoreMap = (lambda x: cv2.addWeighted(get_score_map(cv2.resize(x, ((args.image_size,) * 2))[(:h, :w)]), 0.8, image, 0.2, 0))
                    visScores = (lambda x: [getScoreMap(np.maximum(x, 0)), getScoreMap(np.maximum((- x), 0))])
                    h_images = sum(([[image]] + list(map(visScores, [cam[0], icd_bu[L], icd_bu_sp[L], icd_td[0]]))), [])
                    v_images[L].append(imhstack(h_images, height=120))
                elif (len(v_images[L]) == NUM):
                    img = imvstack(v_images[L])
                    imwrite(os.path.join(args.snapshot, 'results', 'scores_demo', ('class_%d.jpg' % L)), img)
                    v_images[L].append(None)
    for (L, v_images) in enumerate(v_images):
        if (v_images and (v_images[(- 1)] is not None)):
            img = imvstack(v_images)
            imwrite(os.path.join(args.snapshot, 'results', 'scores_demo', ('class_%d.jpg' % L)), img)
