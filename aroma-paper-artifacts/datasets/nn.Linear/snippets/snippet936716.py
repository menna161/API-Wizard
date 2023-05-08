import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim


def __init__(self, user_max_dict, movie_max_dict, convParams, embed_dim=32, fc_size=200):
    "\n\n        Args:\n            user_max_dict: the max value of each user attribute. {'uid': xx, 'gender': xx, 'age':xx, 'job':xx}\n            user_embeds: size of embedding_layers.\n            movie_max_dict: {'mid':xx, 'mtype':18, 'mword':15}\n            fc_sizes: fully connect layer sizes. normally 2\n        "
    super(rec_model, self).__init__()
    self.embedding_uid = nn.Embedding(user_max_dict['uid'], embed_dim)
    self.embedding_gender = nn.Embedding(user_max_dict['gender'], (embed_dim // 2))
    self.embedding_age = nn.Embedding(user_max_dict['age'], (embed_dim // 2))
    self.embedding_job = nn.Embedding(user_max_dict['job'], (embed_dim // 2))
    self.fc_uid = nn.Linear(embed_dim, embed_dim)
    self.fc_gender = nn.Linear((embed_dim // 2), embed_dim)
    self.fc_age = nn.Linear((embed_dim // 2), embed_dim)
    self.fc_job = nn.Linear((embed_dim // 2), embed_dim)
    self.fc_user_combine = nn.Linear((4 * embed_dim), fc_size)
    self.embedding_mid = nn.Embedding(movie_max_dict['mid'], embed_dim)
    self.embedding_mtype_sum = nn.EmbeddingBag(movie_max_dict['mtype'], embed_dim, mode='sum')
    self.fc_mid = nn.Linear(embed_dim, embed_dim)
    self.fc_mtype = nn.Linear(embed_dim, embed_dim)
    self.fc_mid_mtype = nn.Linear((embed_dim * 2), fc_size)
    self.embedding_mwords = nn.Embedding(movie_max_dict['mword'], embed_dim)
    kernel_sizes = convParams['kernel_sizes']
    self.Convs_text = [nn.Sequential(nn.Conv2d(1, 8, kernel_size=(k, embed_dim)), nn.ReLU(), nn.MaxPool2d(kernel_size=(((15 - k) + 1), 1), stride=(1, 1))).to(device) for k in kernel_sizes]
    self.fc_movie_combine = nn.Linear(((embed_dim * 2) + (8 * len(kernel_sizes))), fc_size)
    self.BN_uid = nn.BatchNorm2d(1)
    self.BN_gender = nn.BatchNorm2d(1)
    self.BN_age = nn.BatchNorm2d(1)
    self.BN_job = nn.BatchNorm2d(1)
    self.BN_mid = nn.BatchNorm2d(1)
    self.BN_mtype = nn.BatchNorm2d(1)
