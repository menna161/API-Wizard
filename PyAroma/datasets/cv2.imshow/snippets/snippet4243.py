import argparse
import cv2
import torch
from model import SCNN
from model_ENET_SAD import ENet_SAD
from utils.prob2lines import getLane
from utils.transforms import *
import time
from multiprocessing import Process, JoinableQueue, SimpleQueue
from threading import Lock


def main():
    args = parse_args()
    video_path = args.video_path
    weight_path = args.weight_path
    if pipeline:
        input_queue = JoinableQueue()
        pre_process = Process(target=pre_processor, args=((input_queue, video_path),))
        pre_process.start()
        output_queue = SimpleQueue()
        post_process = Process(target=post_processor, args=((output_queue, args.visualize),))
        post_process.start()
    else:
        cap = cv2.VideoCapture(video_path)
    save_dict = torch.load(weight_path, map_location='cpu')
    net.load_state_dict(save_dict['net'])
    net.eval()
    net.cuda()
    while True:
        if pipeline:
            loop_start = time.time()
            x = input_queue.get()
            input_queue.task_done()
            gpu_start = time.time()
            (seg_pred, exist_pred) = network(net, x)
            gpu_end = time.time()
            output_queue.put((x, seg_pred, exist_pred))
            loop_end = time.time()
        else:
            if (not cap.isOpened()):
                break
            (ret, frame) = cap.read()
            if ret:
                loop_start = time.time()
                frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
                frame = transform_img({'img': frame})['img']
                img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                x = transform_to_net({'img': img})['img']
                x.unsqueeze_(0)
                gpu_start = time.time()
                (seg_pred, exist_pred) = network(net, x)
                gpu_end = time.time()
                seg_pred = seg_pred.numpy()[0]
                exist_pred = exist_pred.numpy()
                exist = [(1 if (exist_pred[(0, i)] > 0.5) else 0) for i in range(4)]
                print(exist)
                for i in getLane.prob2lines_CULane(seg_pred, exist):
                    print(i)
                loop_end = time.time()
                if args.visualize:
                    img = visualize(img, seg_pred, exist_pred)
                    cv2.imshow('input_video', frame)
                    cv2.imshow('output_video', img)
                if ((cv2.waitKey(1) & 255) == ord('q')):
                    break
            else:
                break
        print('gpu_runtime:', (gpu_end - gpu_start), 'FPS:', int((1 / (gpu_end - gpu_start))))
        print('total_runtime:', (loop_end - loop_start), 'FPS:', int((1 / (loop_end - loop_start))))
    cv2.destroyAllWindows()
