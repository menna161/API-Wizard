import os
import cv2
import json
import random
from collections import defaultdict
import panda_utils as util


def showAnns(self, imgrequest=None, range=10, imgfilters=[], shuffle=True, saveimg=False):
    "\n        :param imgrequest: list, images names you want to request, eg. ['1-HIT_canteen/IMG_1_4.jpg', ...]\n        :param range: number of image to show\n        :param imgfilters: essential keywords in image name\n        :param shuffle: shuffle all image\n        :return:\n        "
    savedir = 'results/image'
    if (saveimg and (not os.path.exists(savedir))):
        os.makedirs(savedir)
    if ((imgrequest is None) or (not isinstance(imgrequest, list))):
        allnames = list(self.annos.keys())
        imgnames = ([] if imgfilters else allnames)
        if imgfilters:
            for imgname in allnames:
                iskeep = False
                for imgfilter in imgfilters:
                    if (imgfilter in imgname):
                        iskeep = True
                if iskeep:
                    imgnames.append(imgname)
        if shuffle:
            random.shuffle(imgnames)
        if range:
            if (isinstance(range, int) and (range <= len(imgnames))):
                imgnames = imgnames[:range]
    else:
        imgnames = imgrequest
    for imgname in imgnames:
        imgpath = os.path.join(self.imagepath, imgname)
        img = self.loadImg(imgpath)
        if (img is None):
            continue
        if (self.annomode == 'person'):
            imgwithann = self._addPersonAnns(imgname, img)
        elif (self.annomode == 'vehicle'):
            imgwithann = self._addVehicleAnns(imgname, img)
        elif (self.annomode == 'person&vehicle'):
            imgwithann = self._addPersonVehicleAnns(imgname, img)
        elif (self.annomode == 'headbbox'):
            imgwithann = self._addHeadbboxAnns(imgname, img)
        elif (self.annomode == 'headpoint'):
            imgwithann = self._addHeadpointAnns(imgname, img)
        if saveimg:
            cv2.imwrite(os.path.join(savedir, (util.custombasename(imgname) + '.jpg')), imgwithann)
        cv2.putText(img, 'Press any button to continue', (0, 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        cv2.imshow('image_with_anno', imgwithann)
        cv2.waitKey(0)