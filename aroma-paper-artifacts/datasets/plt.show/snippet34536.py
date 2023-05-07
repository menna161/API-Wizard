import torch
import argparse
from torch.utils.data import DataLoader
from torch import nn, optim
from torchvision.transforms import transforms
from unet import Unet
from dataset import LiverDataset
import matplotlib.pyplot as plt


def test(args):
    model = Unet(3, 1)
    model.load_state_dict(torch.load(args.ckpt, map_location='cpu'))
    liver_dataset = LiverDataset('data/val', transform=x_transforms, target_transform=y_transforms)
    dataloaders = DataLoader(liver_dataset, batch_size=1)
    model.eval()
    import matplotlib.pyplot as plt
    plt.ion()
    with torch.no_grad():
        for (x, _) in dataloaders:
            y = model(x).sigmoid()
            img_y = torch.squeeze(y).numpy()
            plt.imshow(img_y)
            plt.pause(0.01)
        plt.show()
