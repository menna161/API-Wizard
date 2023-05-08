import tensorflow as tf
import numpy as np
import cv2
from psbody.meshlite import Mesh
import cv2
import scipy.io as sio
import ipdb

if (__name__ == '__main__'):
    m = Mesh()
    m.load_from_ply('~/Data/HEVA_Validate/S1_Box_1_C1/Res_1/frame0010.ply')
    import cv2
    img = cv2.imread('~/HEVA_Validate/S1_Box_1_C1/Image/frame0010.png')
    import scipy.io as sio
    cam_data = sio.loadmat('~/Data/HEVA_Validate/S1_Box_1_C1/GT/camera.mat', squeeze_me=True, struct_as_record=False)
    cam_data = cam_data['camera']
    cam = Perspective_Camera(cam_data.focal_length[0], cam_data.focal_length[1], cam_data.principal_pt[0], cam_data.principal_pt[1], (cam_data.t / 1000.0), cam_data.R_angles)
    v = tf.constant(m.v, dtype=tf.float32)
    j2ds = cam.project(v)
    sess = tf.Session()
    sess.run(tf.global_variables_initializer())
    j2ds = sess.run(j2ds)
    import ipdb
    ipdb.set_trace()
    for p in j2ds:
        x = int(p[0])
        y = int(p[1])
        if ((x < 0) or (y < 0)):
            continue
        if ((x < img.shape[0]) and (y < img.shape[1])):
            img[(x, y, :)] = 0
    cv2.imshow('Img', img)
    cv2.waitKey(0)
