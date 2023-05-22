import torch
from models import EfficientDet
from models.efficientnet import EfficientNet

if (__name__ == '__main__'):
    inputs = torch.randn(5, 3, 512, 512)
    model = EfficientNet.from_pretrained('efficientnet-b0')
    inputs = torch.randn(4, 3, 512, 512)
    P = model(inputs)
    for (idx, p) in enumerate(P):
        print('P{}: {}'.format(idx, p.size()))
    model = EfficientDet(num_classes=20, is_training=False)
    output = model(inputs)
    for out in output:
        print(out.size())
