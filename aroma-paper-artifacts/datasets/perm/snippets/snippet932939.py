import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
import numba as nb
import multiprocessing
import torch_scatter


def forward(self, pt_fea, xy_ind, voxel_fea=None):
    cur_dev = pt_fea[0].get_device()
    cat_pt_ind = []
    for i_batch in range(len(xy_ind)):
        cat_pt_ind.append(F.pad(xy_ind[i_batch], (1, 0), 'constant', value=i_batch))
    cat_pt_fea = torch.cat(pt_fea, dim=0)
    cat_pt_ind = torch.cat(cat_pt_ind, dim=0)
    pt_num = cat_pt_ind.shape[0]
    shuffled_ind = torch.randperm(pt_num, device=cur_dev)
    cat_pt_fea = cat_pt_fea[(shuffled_ind, :)]
    cat_pt_ind = cat_pt_ind[(shuffled_ind, :)]
    (unq, unq_inv, unq_cnt) = torch.unique(cat_pt_ind, return_inverse=True, return_counts=True, dim=0)
    unq = unq.type(torch.int64)
    if (self.pt_selection == 'random'):
        grp_ind = grp_range_torch(unq_cnt, cur_dev)[torch.argsort(torch.argsort(unq_inv))]
        remain_ind = (grp_ind < self.max_pt)
    elif (self.pt_selection == 'farthest'):
        unq_ind = np.split(np.argsort(unq_inv.detach().cpu().numpy()), np.cumsum(unq_cnt.detach().cpu().numpy()[:(- 1)]))
        remain_ind = np.zeros((pt_num,), dtype=np.bool)
        np_cat_fea = cat_pt_fea.detach().cpu().numpy()[(:, :3)]
        pool_in = []
        for i_inds in unq_ind:
            if (len(i_inds) > self.max_pt):
                pool_in.append((np_cat_fea[(i_inds, :)], self.max_pt))
        if (len(pool_in) > 0):
            pool = multiprocessing.Pool(multiprocessing.cpu_count())
            FPS_results = pool.starmap(parallel_FPS, pool_in)
            pool.close()
            pool.join()
        count = 0
        for i_inds in unq_ind:
            if (len(i_inds) <= self.max_pt):
                remain_ind[i_inds] = True
            else:
                remain_ind[i_inds[FPS_results[count]]] = True
                count += 1
    cat_pt_fea = cat_pt_fea[(remain_ind, :)]
    cat_pt_ind = cat_pt_ind[(remain_ind, :)]
    unq_inv = unq_inv[remain_ind]
    unq_cnt = torch.clamp(unq_cnt, max=self.max_pt)
    if (self.pt_model == 'pointnet'):
        processed_cat_pt_fea = self.PPmodel(cat_pt_fea)
    if (self.pt_pooling == 'max'):
        pooled_data = torch_scatter.scatter_max(processed_cat_pt_fea, unq_inv, dim=0)[0]
    else:
        raise NotImplementedError
    if self.fea_compre:
        processed_pooled_data = self.fea_compression(pooled_data)
    else:
        processed_pooled_data = pooled_data
    out_data_dim = [len(pt_fea), self.grid_size[0], self.grid_size[1], self.pt_fea_dim]
    out_data = torch.zeros(out_data_dim, dtype=torch.float32).to(cur_dev)
    out_data[(unq[(:, 0)], unq[(:, 1)], unq[(:, 2)], :)] = processed_pooled_data
    out_data = out_data.permute(0, 3, 1, 2)
    if (self.local_pool_op != None):
        out_data = self.local_pool_op(out_data)
    if (voxel_fea is not None):
        out_data = torch.cat((out_data, voxel_fea), 1)
    net_return_data = self.BEV_model(out_data)
    return net_return_data
