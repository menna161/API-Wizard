from datareader import DBreader_Vimeo90k
from torch.utils.data import DataLoader
import argparse
from torchvision import transforms
import torch
from TestModule import Middlebury_other
import models
from trainer import Trainer
import losses
import datetime


def main():
    args = parser.parse_args()
    torch.cuda.set_device(args.gpu_id)
    dataset = DBreader_Vimeo90k(args.train, random_crop=(args.patch_size, args.patch_size))
    TestDB = Middlebury_other(args.test_input, args.gt)
    train_loader = DataLoader(dataset=dataset, batch_size=args.batch_size, shuffle=True, num_workers=0)
    model = models.Model(args)
    loss = losses.Loss(args)
    start_epoch = 0
    if (args.load is not None):
        checkpoint = torch.load(args.load)
        model.load(checkpoint['state_dict'])
        start_epoch = checkpoint['epoch']
    my_trainer = Trainer(args, train_loader, TestDB, model, loss, start_epoch)
    now = datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S')
    with open((args.out_dir + '/config.txt'), 'a') as f:
        f.write((now + '\n\n'))
        for arg in vars(args):
            f.write('{}: {}\n'.format(arg, getattr(args, arg)))
        f.write('\n')
    while (not my_trainer.terminate()):
        my_trainer.train()
        my_trainer.test()
    my_trainer.close()
