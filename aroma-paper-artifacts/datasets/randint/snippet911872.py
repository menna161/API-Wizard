import math
import random


def __call__(self, img):
    if (random.uniform(0, 1) > self.probability):
        return img
    for attempt in range(100):
        area = (img.size()[1] * img.size()[2])
        target_area = (random.uniform(self.sl, self.sh) * area)
        aspect_ratio = random.uniform(self.r1, (1 / self.r1))
        h = int(round(math.sqrt((target_area * aspect_ratio))))
        w = int(round(math.sqrt((target_area / aspect_ratio))))
        if ((w < img.size()[2]) and (h < img.size()[1])):
            x1 = random.randint(0, (img.size()[1] - h))
            y1 = random.randint(0, (img.size()[2] - w))
            if (img.size()[0] == 3):
                img[(0, x1:(x1 + h), y1:(y1 + w))] = self.mean[0]
                img[(1, x1:(x1 + h), y1:(y1 + w))] = self.mean[1]
                img[(2, x1:(x1 + h), y1:(y1 + w))] = self.mean[2]
            else:
                img[(0, x1:(x1 + h), y1:(y1 + w))] = self.mean[0]
            return img
    return img
