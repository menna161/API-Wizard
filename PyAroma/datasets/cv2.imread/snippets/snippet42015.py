import cv2
import numpy as np
import os
import argparse
from os.path import isfile, join


def convert_frames_to_video(args):
    frame_array = []
    files = []
    for i in range(args.frames):
        if args.const:
            files.append((str(args.start_cnt) + args.ext))
        elif (not args.reverse):
            files.append((str((args.start_cnt + i)) + args.ext))
        else:
            files.append((str((((args.start_cnt + args.frames) - i) - 1)) + args.ext))
    print(files)
    for i in range(len(files)):
        filename = (args.input + files[i])
        img = cv2.imread(filename)
        (height, width, layers) = img.shape
        size = (width, height)
        print(filename)
        frame_array.append(img)
    out = cv2.VideoWriter(args.out, cv2.VideoWriter_fourcc(*'DIVX'), args.fps, size)
    for i in range(len(frame_array)):
        out.write(frame_array[i])
    out.release()
