import numpy as np


def gen_box_data(trainset, y_train, length=1000, image_size=32, box_size=4, offset1=7, offset2=23, shiftdiv=6):
    '\n    * Generates training set which has colored 2 boxes (green and red) in each image.\n    * There are two classes:\n        1. Red-to-the-left-of-Green\n        2. Green-to-the-left-of-Red\n    \n    * Input arguments:   \n        trainset -- empty numpy array with size of your input training images [dataset_size, channel, width, height]\n        y_train -- empty numpy array with size of your input training labels [data_size]\n        length -- number of images in the dataset [data_size]\n        image_size -- spatial size of image \n        box_size -- spatial size of box (square)\n        offset1 -- offset for class 1\n        offset2 --  offset for class 2\n        shiftdiv -- division of shift to fluctuate the location around the offset on the y-axis\n\n    * Output arguments:\n        trainset -- numpy array with size of generated input training images [dataset_size, channel, width, height]\n        y_train -- numpy array with size of generated input training labels [data_size]\n    '
    np.random.seed(1988)
    img = np.zeros([3, image_size, image_size], dtype=float)
    patch = np.ones([box_size, box_size], dtype=float)
    off_size = (image_size - box_size)
    for i in range(length):
        if ((i % 2) == 0):
            im = img.copy()
            offsetx = np.random.randint(((off_size / 2) - box_size))
            offsety = (np.random.randint(((- off_size) / shiftdiv), (off_size / shiftdiv)) + offset1)
            im[(0, offsety:(offsety + box_size), offsetx:(offsetx + box_size))] = patch
            offsetx2 = np.random.randint(offsetx, off_size)
            offsety2 = (np.random.randint(((- off_size) / shiftdiv), (off_size / shiftdiv)) + offset1)
            while (abs((offsetx - offsetx2)) < (box_size + 1)):
                offsetx2 = np.random.randint(offsetx, off_size)
                offsety2 = (np.random.randint(((- off_size) / shiftdiv), (off_size / shiftdiv)) + offset1)
            im[(1, offsety2:(offsety2 + box_size), offsetx2:(offsetx2 + box_size))] = patch
            trainset[i] = im
            y_train[i] = 0
        elif ((i % 2) == 1):
            im = img.copy()
            offsetx = np.random.randint(((off_size / 2) - box_size))
            offsety = (np.random.randint(((- off_size) / shiftdiv), (off_size / shiftdiv)) + offset2)
            im[(1, offsety:(offsety + box_size), offsetx:(offsetx + box_size))] = patch
            offsetx2 = np.random.randint(offsetx, off_size)
            offsety2 = (np.random.randint(((- off_size) / shiftdiv), (off_size / shiftdiv)) + offset2)
            while (abs((offsetx - offsetx2)) < (box_size + 1)):
                offsetx2 = np.random.randint(offsetx, off_size)
                offsety2 = (np.random.randint(((- off_size) / shiftdiv), (off_size / shiftdiv)) + offset2)
            im[(0, offsety2:(offsety2 + box_size), offsetx2:(offsetx2 + box_size))] = patch
            trainset[i] = im
            y_train[i] = 1
    return (trainset, y_train)
