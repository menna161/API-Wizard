import torch
import torch.nn.functional as F
import math
import argparse
import numpy as np
import os
from DSAN import DSAN
import data_loader

if (__name__ == '__main__'):
    args = get_args()
    print(vars(args))
    SEED = args.seed
    np.random.seed(SEED)
    torch.manual_seed(SEED)
    torch.cuda.manual_seed_all(SEED)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False
    os.environ['CUDA_VISIBLE_DEVICES'] = args.gpu
    dataloaders = load_data(args.root_path, args.src, args.tar, args.batch_size)
    model = DSAN(num_classes=args.nclass).cuda()
    correct = 0
    stop = 0
    if args.bottleneck:
        optimizer = torch.optim.SGD([{'params': model.feature_layers.parameters()}, {'params': model.bottle.parameters(), 'lr': args.lr[1]}, {'params': model.cls_fc.parameters(), 'lr': args.lr[2]}], lr=args.lr[0], momentum=args.momentum, weight_decay=args.decay)
    else:
        optimizer = torch.optim.SGD([{'params': model.feature_layers.parameters()}, {'params': model.cls_fc.parameters(), 'lr': args.lr[1]}], lr=args.lr[0], momentum=args.momentum, weight_decay=args.decay)
    for epoch in range(1, (args.nepoch + 1)):
        stop += 1
        for (index, param_group) in enumerate(optimizer.param_groups):
            param_group['lr'] = (args.lr[index] / math.pow((1 + ((10 * (epoch - 1)) / args.nepoch)), 0.75))
        train_epoch(epoch, model, dataloaders, optimizer)
        t_correct = test(model, dataloaders[(- 1)])
        if (t_correct > correct):
            correct = t_correct
            stop = 0
            torch.save(model, 'model.pkl')
        print(f'''{args.src}-{args.tar}: max correct: {correct} max accuracy: {((100.0 * correct) / len(dataloaders[(- 1)].dataset)):.2f}%
''')
        if (stop >= args.early_stop):
            print(f'Final test acc: {((100.0 * correct) / len(dataloaders[(- 1)].dataset)):.2f}%')
            break
