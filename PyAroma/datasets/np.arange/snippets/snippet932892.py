import numpy as np
import torch
import random
from plyfile import PlyData
from torch.utils import data
from xml.dom import minidom


def __init__(self, data_path, sample_interval, time_step, label_convert_fun=None, return_ref=False, crop_data=None):
    'Initialization'
    self.return_ref = return_ref
    self.crop_data = crop_data
    plydata = PlyData.read(data_path)
    self.xyz = np.array(np.transpose(np.stack((plydata['vertex']['x'], plydata['vertex']['y'], plydata['vertex']['z'])))).astype(np.float32)
    try:
        self.class_id = np.array(plydata['vertex']['class'])
    except:
        self.class_id = np.zeros_like(plydata['vertex']['x'], dtype=int)
    if label_convert_fun:
        self.class_id = label_convert_fun(self.class_id)
    GPS_time = plydata['vertex']['GPS_time']
    sample_start_times = np.arange((GPS_time[0] + sample_interval), (GPS_time[(- 1)] - sample_interval), time_step)
    start_ind = np.searchsorted(GPS_time, (sample_start_times - sample_interval))
    end_ind = np.searchsorted(GPS_time, (sample_start_times + sample_interval))
    end_ind[(- 1)] = np.size(GPS_time)
    self.start_end = np.transpose(np.stack((start_ind, end_ind)))
    self.start_end = np.unique(self.start_end, axis=0)
    remain_ind = ((self.start_end[(:, 1)] - self.start_end[(:, 0)]) > 1000)
    self.start_end = self.start_end[(remain_ind, :)]
    if self.crop_data:
        remain_ind = ((self.start_end[(:, 1)] - self.start_end[(:, 0)]) > crop_data)
        self.start_end = self.start_end[(remain_ind, :)]
    if self.return_ref:
        self.reflectance = np.array(plydata['vertex']['reflectance']).astype(np.float32)
