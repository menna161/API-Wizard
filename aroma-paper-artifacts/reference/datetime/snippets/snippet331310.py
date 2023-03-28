import datetime
import re
import os
import csv
import json
from tensorboardX import SummaryWriter
from argparse import Namespace


def __init__(self, args):
    time_signature = str(datetime.datetime.now())[:19]
    time_signature = re.sub('[^0-9]', '_', time_signature)
    signature = '{}_{}_{}'.format(time_signature, args.model_name, args.dataset_name)
    self.dir = './runs/{}/'.format(signature)
    if (not os.path.exists(self.dir)):
        os.makedirs(self.dir)
    settings_dict = vars(args)
    with open((self.dir + 'settings.json'), 'w') as file:
        json.dump(settings_dict, file, sort_keys=True, indent=4)
    with open((self.dir + 'train_metrics.csv'), 'w') as file:
        filewriter = csv.writer(file, delimiter=';')
        filewriter.writerow(['epoch', 'train_loss', 'val_loss', 'top1_percent', 'top5_percent', 'top10_percent', 'top25_percent'])
    self.tensorboard = args.tensorboard
    if self.tensorboard:
        self.writer = SummaryWriter(log_dir=(self.dir + 'tensorboard/'))
        self.k = 0
