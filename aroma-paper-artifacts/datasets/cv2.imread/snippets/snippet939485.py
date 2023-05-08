import os
import pickle as pkl
import scipy.io as sio
import numpy as np
from camera import Perspective_Camera
import cv2


def load_data(img_path, num_view):
    imgs = []
    j2ds = []
    segs = []
    cams = []
    for i in range(1, (num_view + 1)):
        img_i_path = img_path.replace('_C1', ('_C' + str(i)))
        img_i = cv2.imread(img_i_path)
        imgs.append(img_i)
        j2d_i_path = img_i_path.replace('Image', 'Pose_2D')
        j2d_i_path = j2d_i_path.replace('.png', '.png_pose.npz')
        j2d_i = np.load(j2d_i_path)
        j2d_i = j2d_i['pose'].T[(:, :2)]
        j2ds.append(j2d_i)
        "\n\t\tseg_i_path = img_i_path.replace('Image', 'Segmentation')\n\t\tseg_i_path = seg_i_path.replace('.png', '.png_segmentation.npz_vis.png')\n\t\tseg_i = cv2.imread(seg_i_path)\n\t\tseg_i = cv2.split(seg_i)[0]\n\t\tseg_i[seg_i > 0] = 1\n\t\tsegs.append(seg_i)\n\t\t"
        segs.append(None)
        cam_i_path = img_i_path.replace('Image', 'GT')
        cam_i_path = os.path.join(os.path.dirname(cam_i_path), 'camera.mat')
        cam_i = sio.loadmat(cam_i_path, squeeze_me=True, struct_as_record=False)
        cam_i = cam_i['camera']
        cam = Perspective_Camera(cam_i.focal_length[0], cam_i.focal_length[1], cam_i.principal_pt[0], cam_i.principal_pt[1], (cam_i.t / 1000.0), cam_i.R_angles)
        cams.append(cam)
    j2ds = np.array(j2ds)
    return (imgs, j2ds, segs, cams)
