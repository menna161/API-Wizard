import torch


def __iter__(self):
    img_ratios = torch.tensor(self.img_ratios)
    tall_indices = (img_ratios < 1).nonzero().view((- 1))
    fat_indices = (img_ratios >= 1).nonzero().view((- 1))
    tall_indices_length = len(tall_indices)
    fat_indices_length = len(fat_indices)
    tall_indices = tall_indices[torch.randperm(tall_indices_length)]
    fat_indices = fat_indices[torch.randperm(fat_indices_length)]
    num_tall_remainder = (tall_indices_length % self.batch_size)
    num_fat_remainder = (fat_indices_length % self.batch_size)
    tall_indices = tall_indices[:(tall_indices_length - num_tall_remainder)]
    fat_indices = fat_indices[:(fat_indices_length - num_fat_remainder)]
    tall_indices = tall_indices.view((- 1), self.batch_size)
    fat_indices = fat_indices.view((- 1), self.batch_size)
    merge_indices = torch.cat([tall_indices, fat_indices], dim=0)
    merge_indices = merge_indices[torch.randperm(len(merge_indices))].view((- 1))
    return iter(merge_indices.tolist())
