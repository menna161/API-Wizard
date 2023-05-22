import torch
import torch.nn as nn

if (__name__ == '__main__'):
    im = torch.randn(1, 3, 572, 572)
    model = SimpleUnet()
    x = model(im)
