import os
import cv2
import json
import random
from collections import defaultdict
import panda_utils as util


def saveVideo(self, videorequest=None, withanno=True, maxframe=None):
    "\n        :param maxframe: maximum frame number for each video\n        :param withanno: add annotation on video to save or not\n        :param videorequest: list, sequence names you want to request, eg. ['1-HIT_Canteen_frames', ...]\n        :return:\n        "
    if ((videorequest is None) or (not isinstance(videorequest, list))):
        seqnames = self.seqnames
    else:
        seqnames = videorequest
    for seqname in seqnames:
        framespath = os.path.join(self.seqspath, seqname)
        annopath = os.path.join(self.annopath, seqname, self.annofile)
        seqinfopath = os.path.join(self.annopath, seqname, self.seqinfofile)
        print('Loading annotation json file: {}'.format(annopath))
        with open(annopath, 'r') as load_f:
            anno = json.load(load_f)
        with open(seqinfopath, 'r') as load_f:
            seqinfo = json.load(load_f)
        framerate = seqinfo['frameRate']
        width = seqinfo['imWidth']
        height = seqinfo['imHeight']
        frames = seqinfo['imUrls']
        save_height = int(((self.videowidth / width) * height))
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter(os.path.join(self.savepath, (seqname + '.avi')), fourcc, framerate, (self.videowidth, save_height), True)
        for (i, frame) in enumerate(frames):
            print('writing frame {} to video.'.format(frame))
            imgpath = os.path.join(framespath, frame)
            img = cv2.imread(imgpath)
            img = cv2.resize(img, (self.videowidth, save_height))
            if withanno:
                img = self.addanno(img, (i + 1), anno, (self.videowidth, save_height))
            cv2.imwrite(os.path.join(self.savepath, (str(i) + '.jpg')), img)
            out.write(img)
            if (isinstance(maxframe, int) and ((i + 1) == maxframe)):
                break
        out.release()
