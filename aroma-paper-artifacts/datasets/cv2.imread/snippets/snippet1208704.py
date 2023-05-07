from __future__ import print_function
import sys
import os
import argparse
import torch
import torch.nn as nn
import torch.backends.cudnn as cudnn
import torchvision.transforms as transforms
from torch.autograd import Variable
from data import WIDERFace_ROOT, WIDERFace_CLASSES as labelmap
from PIL import Image
from data import WIDERFaceDetection, WIDERFaceAnnotationTransform, WIDERFace_CLASSES, WIDERFace_ROOT, BaseTransform, TestBaseTransform
from data import *
import torch.utils.data as data
from light_face_ssd import build_ssd
import pdb
import numpy as np
import cv2
import math
import matplotlib.pyplot as plt
import time


def light_test_oneimage():
    cfg = widerface_640
    num_classes = (len(WIDERFace_CLASSES) + 1)
    net = build_ssd('test', cfg['min_dim'], num_classes)
    net.load_state_dict(torch.load(args.trained_model))
    net.cuda()
    net.eval()
    print('Finished loading model!')
    cuda = args.cuda
    transform = TestBaseTransform((104, 117, 123))
    thresh = cfg['conf_thresh']
    path = './data/yuebing.jpg'
    img_id = 'result'
    img = cv2.imread(path, cv2.IMREAD_COLOR)
    shrink = 1
    det = infer(net, img, transform, thresh, cuda, shrink)
    vis_detections(img, det, img_id, 0.6)
