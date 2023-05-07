import argparse
from core.model.vgg import vgg16_cam
from core.utils import *
from core.data.VOC import ClassLoader
import multiprocessing as mp
from subprocess import call


def demo(args, num, savename):
    palette = np.random.randint(0, 256, (1000, 3)).astype(np.uint8)
    with open(args.data_list) as f:
        names = [x.strip() for x in f.readlines()]
    demo_images = []
    for name in names[:num]:
        img = cv2.imread(os.path.join(args.image_root, (name + '.jpg')))
        sp0 = cv2.imread(os.path.join(args.superpixel_root, (name + '.png'))).astype(np.int32)
        sp1 = cv2.imread(os.path.join(args.save_superpixel_root, (name + '.png'))).astype(np.int32)
        sp0 = ((sp0[(..., 0)] + (sp0[(..., 1)] * 256)) + (sp0[(..., 2)] * 65536))
        sp1 = ((sp1[(..., 0)] + (sp1[(..., 1)] * 256)) + (sp1[(..., 2)] * 65536))
        sp0 = palette[sp0.ravel()].reshape(img.shape)
        sp1 = palette[sp1.ravel()].reshape(img.shape)
        demo_images.append(imhstack([img, sp0, sp1], height=240))
    demo_images = imvstack(demo_images)
    imwrite(savename, demo_images)
