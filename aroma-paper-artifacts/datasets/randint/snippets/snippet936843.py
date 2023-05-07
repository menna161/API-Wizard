import torch.utils.data as data
import random
from PIL import ImageFile
from dataset.augmentation import SSJAugmentation
from dataset.Parsers.MOT17 import GTParser_MOT_17


def __getitem__(self, item):
    item = (item % len(self.parser))
    (image, img_meta, tubes, labels, start_frame) = self.parser[item]
    while (image is None):
        (image, img_meta, tubes, labels, start_frame) = self.parser[((item + random.randint((- 10), 10)) % len(self.parser))]
        print('None processing.')
    if (self.transform is None):
        return (image, img_meta, tubes, labels, start_frame)
    else:
        (image, img_meta, tubes, labels, start_frame) = self.transform(image, img_meta, tubes, labels, start_frame)
        return (image, img_meta, tubes, labels, start_frame)
