import argparse
import json
import os
import shutil
import time
import torch.optim as optim
from torch.utils.data import DataLoader
from tqdm import tqdm
from config import *
import dataset
from model import SCNN
from model_ENET_SAD import ENet_SAD
from utils.tensorboard import TensorBoard
from utils.transforms import *
from utils.lr_scheduler import PolyLR
from multiprocessing import Process, JoinableQueue
from threading import Lock
import pickle


def val(epoch):
    global best_val_loss
    print('Val Epoch: {}'.format(epoch))
    net.eval()
    val_loss = 0
    val_loss_seg = 0
    val_loss_exist = 0
    progressbar = tqdm(range(len(val_loader)))
    with torch.no_grad():
        for (batch_idx, sample) in enumerate(val_loader):
            img = sample['img'].to(device)
            segLabel = sample['segLabel'].to(device)
            exist = sample['exist'].to(device)
            (seg_pred, exist_pred, loss_seg, loss_exist, loss) = net(img, segLabel, exist)
            if isinstance(net, torch.nn.DataParallel):
                loss_seg = loss_seg.sum()
                loss_exist = loss_exist.sum()
                loss = loss.sum()
            gap_num = 5
            if (((batch_idx % gap_num) == 0) and (batch_idx < (50 * gap_num))):
                origin_imgs = []
                seg_pred = seg_pred.detach().cpu().numpy()
                exist_pred = exist_pred.detach().cpu().numpy()
                for b in range(len(img)):
                    img_name = sample['img_name'][b]
                    img = cv2.imread(img_name)
                    img = transform_val_img({'img': img})['img']
                    lane_img = np.zeros_like(img)
                    color = np.array([[255, 125, 0], [0, 255, 0], [0, 0, 255], [0, 255, 255]], dtype='uint8')
                    coord_mask = np.argmax(seg_pred[b], axis=0)
                    for i in range(0, 4):
                        if (exist_pred[(b, i)] > 0.5):
                            lane_img[(coord_mask == (i + 1))] = color[i]
                    img = cv2.addWeighted(src1=lane_img, alpha=0.8, src2=img, beta=1.0, gamma=0.0)
                    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                    lane_img = cv2.cvtColor(lane_img, cv2.COLOR_BGR2RGB)
                    cv2.putText(lane_img, '{}'.format([(1 if (exist_pred[(b, i)] > 0.5) else 0) for i in range(4)]), (20, 20), cv2.FONT_HERSHEY_SIMPLEX, 1.1, (255, 255, 255), 2)
                    origin_imgs.append(img)
                    origin_imgs.append(lane_img)
                tensorboard.image_summary('img_{}'.format(batch_idx), origin_imgs, epoch)
            val_loss += loss.item()
            val_loss_seg += loss_seg.item()
            val_loss_exist += loss_exist.item()
            progressbar.set_description('batch loss: {:.3f}'.format(loss.item()))
            progressbar.update(1)
    progressbar.close()
    iter_idx = ((epoch + 1) * len(train_loader))
    tensorboard.scalar_summary('val_loss', val_loss, iter_idx)
    tensorboard.scalar_summary('val_loss_seg', val_loss_seg, iter_idx)
    tensorboard.scalar_summary('val_loss_exist', val_loss_exist, iter_idx)
    tensorboard.writer.flush()
    print('------------------------\n')
    if (val_loss < best_val_loss):
        best_val_loss = val_loss
        save_name = os.path.join(exp_dir, (exp_name + '.pth'))
        copy_name = os.path.join(exp_dir, (exp_name + '_best.pth'))
        shutil.copyfile(save_name, copy_name)
