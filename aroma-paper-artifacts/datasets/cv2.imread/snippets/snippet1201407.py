import argparse
import os
import cv2
import rasterio
import shapely
import skimage
import numpy as np
from skimage import measure
from skimage.morphology import watershed
import pandas as pd
from tqdm import tqdm
import rasterio.features
import shapely.wkt
import shapely.ops
import shapely.geometry


def _internal_test(mask_dir, out_file):
    fn_out = out_file
    with open(fn_out, 'w') as f:
        f.write('ImageId,BuildingId,PolygonWKT_Pix,Confidence\n')
        test_image_list = os.listdir(os.path.join(mask_dir))
        for (idx, image_id) in tqdm(enumerate(test_image_list), total=len(test_image_list)):
            img1 = cv2.imread(os.path.join(mask_dir, image_id), cv2.IMREAD_UNCHANGED)
            labels = img1.astype(np.uint16)
            df_poly = mask_to_poly(labels, min_polygon_area_th=MIN_AREA)
            if (len(df_poly) > 0):
                for (i, row) in df_poly.iterrows():
                    line = '{},{},"{}",{:.6f}\n'.format(image_id.lstrip('Pan-Sharpen_').rstrip('.tif'), row.bid, row.wkt, row.area_ratio)
                    line = _remove_interiors(line)
                    f.write(line)
            else:
                f.write('{},{},{},0\n'.format(image_id, (- 1), 'POLYGON EMPTY'))
