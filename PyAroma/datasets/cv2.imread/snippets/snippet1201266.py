import sys
from os import path, mkdir, listdir, makedirs
import numpy as np
import random
import timeit
import cv2
from tqdm import tqdm
from skimage import measure
from skimage.morphology import square, erosion, dilation
from skimage.morphology import remove_small_objects, watershed, remove_small_holes
from skimage.color import label2rgb
from scipy import ndimage
import pandas as pd
from sklearn.model_selection import KFold
from shapely.wkt import dumps
from shapely.geometry import shape, Polygon
from collections import defaultdict

if (__name__ == '__main__'):
    t0 = timeit.default_timer()
    sub_name = 'submission.csv'
    if (len(sys.argv) > 1):
        sub_name = sys.argv[2]
    df = []
    for fid in tqdm(listdir(lgbm_pred)):
        y_pred = cv2.imread(path.join(lgbm_pred, fid), cv2.IMREAD_UNCHANGED)
        if (y_pred.max() > 0):
            for i in range(1, (y_pred.max() + 1)):
                mask = (255 * (y_pred == i))
                mask = mask.astype('uint8')
                wkt = mask_to_polygons(mask)
                df.append({'ImageId': fid.split('.tif')[0], 'BuildingId': i, 'PolygonWKT_Pix': wkt, 'Confidence': 1})
        else:
            df.append({'ImageId': fid.split('.tif')[0], 'BuildingId': (- 1), 'PolygonWKT_Pix': 'POLYGON EMPTY', 'Confidence': 1})
    df = pd.DataFrame(df, columns=['ImageId', 'BuildingId', 'PolygonWKT_Pix', 'Confidence'])
    df.to_csv(('/wdata/' + sub_name), index=False)
    elapsed = (timeit.default_timer() - t0)
    print('Time: {:.3f} min'.format((elapsed / 60)))
