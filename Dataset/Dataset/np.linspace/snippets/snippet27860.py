import argparse
import numpy as np
from PIL import Image
import torch
import torch.nn as nn
from .utils import *
from facenet_pytorch import MTCNN
from unsup3d.renderer import Renderer


def render_animation(self):
    print(f'Rendering video animations')
    (b, h, w) = self.canon_depth.shape
    morph_frames = 15
    view_zero = torch.FloatTensor([(((0.15 * np.pi) / 180) * 60), 0, 0, 0, 0, 0]).to(self.canon_depth.device)
    morph_s = torch.linspace(0, 1, morph_frames).to(self.canon_depth.device)
    view_morph = ((morph_s.view((- 1), 1, 1) * view_zero.view(1, 1, (- 1))) + ((1 - morph_s.view((- 1), 1, 1)) * self.view.unsqueeze(0)))
    yaw_frames = 80
    yaw_rotations = np.linspace(((- np.pi) / 2), (np.pi / 2), yaw_frames)
    view_after = torch.cat([view_morph, view_zero.repeat(yaw_frames, b, 1)], 0)
    yaw_rotations = np.concatenate([np.zeros(morph_frames), yaw_rotations], 0)

    def rearrange_frames(frames):
        morph_seq = frames[(:, :morph_frames)]
        yaw_seq = frames[(:, morph_frames:)]
        out_seq = torch.cat([morph_seq[(:, :1)].repeat(1, 5, 1, 1, 1), morph_seq, morph_seq[(:, (- 1):)].repeat(1, 5, 1, 1, 1), yaw_seq[(:, (yaw_frames // 2):)], yaw_seq.flip(1), yaw_seq[(:, :(yaw_frames // 2))], morph_seq[(:, (- 1):)].repeat(1, 5, 1, 1, 1), morph_seq.flip(1), morph_seq[(:, :1)].repeat(1, 5, 1, 1, 1)], 1)
        return out_seq
    front_light = torch.FloatTensor([0, 0, 1]).to(self.canon_depth.device)
    canon_shape_im = (self.canon_normal * front_light.view(1, 1, 1, 3)).sum(3).clamp(min=0).unsqueeze(1)
    canon_shape_im = (canon_shape_im.repeat(1, 3, 1, 1) * 0.7)
    shape_animation = self.renderer.render_yaw(canon_shape_im, self.canon_depth, v_after=view_after, rotations=yaw_rotations)
    self.shape_animation = rearrange_frames(shape_animation)
    canon_normal_im = ((self.canon_normal.permute(0, 3, 1, 2) / 2) + 0.5)
    normal_animation = self.renderer.render_yaw(canon_normal_im, self.canon_depth, v_after=view_after, rotations=yaw_rotations)
    self.normal_animation = rearrange_frames(normal_animation)
    texture_animation = self.renderer.render_yaw(((self.canon_im / 2) + 0.5), self.canon_depth, v_after=view_after, rotations=yaw_rotations)
    self.texture_animation = rearrange_frames(texture_animation)
