from model.deeplab import Deeplab
from model.fcn8s import VGG16_FCN8s
from model.discriminator import FCDiscriminator
import torch.optim as optim


def CreateModel(args):
    if (args.model == 'DeepLab'):
        model = Deeplab(num_classes=args.num_classes, init_weights=args.init_weights, restore_from=args.restore_from, phase=args.set)
        if (args.set == 'train'):
            optimizer = optim.SGD(model.optim_parameters(args), lr=args.learning_rate, momentum=args.momentum, weight_decay=args.weight_decay)
            optimizer.zero_grad()
            return (model, optimizer)
        else:
            return model
    if (args.model == 'VGG'):
        model = VGG16_FCN8s(num_classes=19, init_weights=args.init_weights, restore_from=args.restore_from)
        if (args.set == 'train'):
            optimizer = optim.Adam([{'params': model.get_parameters(bias=False)}, {'params': model.get_parameters(bias=True), 'lr': (args.learning_rate * 2)}], lr=args.learning_rate, betas=(0.9, 0.99))
            optimizer.zero_grad()
            return (model, optimizer)
        else:
            return model
