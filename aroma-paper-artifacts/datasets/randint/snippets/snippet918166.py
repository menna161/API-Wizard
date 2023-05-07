from collections import OrderedDict
from batchgenerators.augmentations.utils import random_crop_2D_image_batched, pad_nd_image
import numpy as np
from batchgenerators.dataloading import SlimDataLoaderBase
from multiprocessing import Pool
from nnunet.configuration import default_num_threads
from nnunet.paths import preprocessing_output_dir
from batchgenerators.utilities.file_and_folder_operations import *


def generate_train_batch(self):
    selected_keys = np.random.choice(self.list_of_keys, self.batch_size, True, None)
    data = []
    seg = []
    case_properties = []
    for (j, i) in enumerate(selected_keys):
        if self.get_do_oversample(j):
            force_fg = True
        else:
            force_fg = False
        case_properties.append(self._data[i]['properties'])
        if isfile((self._data[i]['data_file'][:(- 4)] + '.npy')):
            case_all_data = np.load((self._data[i]['data_file'][:(- 4)] + '.npy'), self.memmap_mode)
        else:
            case_all_data = np.load(self._data[i]['data_file'])['data']
        if self.has_prev_stage:
            if isfile((self._data[i]['seg_from_prev_stage_file'][:(- 4)] + '.npy')):
                segs_from_previous_stage = np.load((self._data[i]['seg_from_prev_stage_file'][:(- 4)] + '.npy'), mmap_mode=self.memmap_mode)[None]
            else:
                segs_from_previous_stage = np.load(self._data[i]['seg_from_prev_stage_file'])['data'][None]
            seg_key = np.random.choice(segs_from_previous_stage.shape[0])
            seg_from_previous_stage = segs_from_previous_stage[seg_key:(seg_key + 1)]
            assert all([(i == j) for (i, j) in zip(seg_from_previous_stage.shape[1:], case_all_data.shape[1:])]), ('seg_from_previous_stage does not match the shape of case_all_data: %s vs %s' % (str(seg_from_previous_stage.shape[1:]), str(case_all_data.shape[1:])))
        else:
            seg_from_previous_stage = None
        need_to_pad = self.need_to_pad
        for d in range(3):
            if ((need_to_pad[d] + case_all_data.shape[(d + 1)]) < self.patch_size[d]):
                need_to_pad[d] = (self.patch_size[d] - case_all_data.shape[(d + 1)])
        shape = case_all_data.shape[1:]
        lb_x = ((- need_to_pad[0]) // 2)
        ub_x = (((shape[0] + (need_to_pad[0] // 2)) + (need_to_pad[0] % 2)) - self.patch_size[0])
        lb_y = ((- need_to_pad[1]) // 2)
        ub_y = (((shape[1] + (need_to_pad[1] // 2)) + (need_to_pad[1] % 2)) - self.patch_size[1])
        lb_z = ((- need_to_pad[2]) // 2)
        ub_z = (((shape[2] + (need_to_pad[2] // 2)) + (need_to_pad[2] % 2)) - self.patch_size[2])
        if (not force_fg):
            bbox_x_lb = np.random.randint(lb_x, (ub_x + 1))
            bbox_y_lb = np.random.randint(lb_y, (ub_y + 1))
            bbox_z_lb = np.random.randint(lb_z, (ub_z + 1))
        else:
            foreground_classes = np.array(self._data[i]['properties']['classes'])
            foreground_classes = foreground_classes[(foreground_classes > 0)]
            if (len(foreground_classes) == 0):
                selected_class = 0
            else:
                selected_class = np.random.choice(foreground_classes)
            voxels_of_that_class = np.argwhere((case_all_data[(- 1)] == selected_class))
            if (len(voxels_of_that_class) != 0):
                selected_voxel = voxels_of_that_class[np.random.choice(len(voxels_of_that_class))]
                bbox_x_lb = max(lb_x, (selected_voxel[0] - (self.patch_size[0] // 2)))
                bbox_y_lb = max(lb_y, (selected_voxel[1] - (self.patch_size[1] // 2)))
                bbox_z_lb = max(lb_z, (selected_voxel[2] - (self.patch_size[2] // 2)))
            else:
                bbox_x_lb = np.random.randint(lb_x, (ub_x + 1))
                bbox_y_lb = np.random.randint(lb_y, (ub_y + 1))
                bbox_z_lb = np.random.randint(lb_z, (ub_z + 1))
        bbox_x_ub = (bbox_x_lb + self.patch_size[0])
        bbox_y_ub = (bbox_y_lb + self.patch_size[1])
        bbox_z_ub = (bbox_z_lb + self.patch_size[2])
        valid_bbox_x_lb = max(0, bbox_x_lb)
        valid_bbox_x_ub = min(shape[0], bbox_x_ub)
        valid_bbox_y_lb = max(0, bbox_y_lb)
        valid_bbox_y_ub = min(shape[1], bbox_y_ub)
        valid_bbox_z_lb = max(0, bbox_z_lb)
        valid_bbox_z_ub = min(shape[2], bbox_z_ub)
        case_all_data = case_all_data[(:, valid_bbox_x_lb:valid_bbox_x_ub, valid_bbox_y_lb:valid_bbox_y_ub, valid_bbox_z_lb:valid_bbox_z_ub)]
        if (seg_from_previous_stage is not None):
            seg_from_previous_stage = seg_from_previous_stage[(:, valid_bbox_x_lb:valid_bbox_x_ub, valid_bbox_y_lb:valid_bbox_y_ub, valid_bbox_z_lb:valid_bbox_z_ub)]
        case_all_data_donly = np.pad(case_all_data[:(- 1)], ((0, 0), ((- min(0, bbox_x_lb)), max((bbox_x_ub - shape[0]), 0)), ((- min(0, bbox_y_lb)), max((bbox_y_ub - shape[1]), 0)), ((- min(0, bbox_z_lb)), max((bbox_z_ub - shape[2]), 0))), self.pad_mode, **self.pad_kwargs_data)
        case_all_data_segonly = np.pad(case_all_data[(- 1):], ((0, 0), ((- min(0, bbox_x_lb)), max((bbox_x_ub - shape[0]), 0)), ((- min(0, bbox_y_lb)), max((bbox_y_ub - shape[1]), 0)), ((- min(0, bbox_z_lb)), max((bbox_z_ub - shape[2]), 0))), 'constant', **{'constant_values': (- 1)})
        if (seg_from_previous_stage is not None):
            seg_from_previous_stage = np.pad(seg_from_previous_stage, ((0, 0), ((- min(0, bbox_x_lb)), max((bbox_x_ub - shape[0]), 0)), ((- min(0, bbox_y_lb)), max((bbox_y_ub - shape[1]), 0)), ((- min(0, bbox_z_lb)), max((bbox_z_ub - shape[2]), 0))), 'constant', **{'constant_values': 0})
            case_all_data_segonly = np.concatenate((case_all_data_segonly, seg_from_previous_stage), 0)
        data.append(case_all_data_donly[None])
        seg.append(case_all_data_segonly[None])
    data = np.vstack(data)
    seg = np.vstack(seg)
    return {'data': data, 'seg': seg, 'properties': case_properties, 'keys': selected_keys}
