import random
import torch


def query(self, images):
    'Return an image from the pool.\n\n        Parameters:\n            images: the latest generated images from the generator\n\n        Returns images from the buffer.\n\n        By 50/100, the buffer will return input images.\n        By 50/100, the buffer will return images previously stored in the buffer,\n        and insert the current images to the buffer.\n        '
    if (self.pool_size == 0):
        return images
    return_images = []
    for image in images:
        image = torch.unsqueeze(image.data, 0)
        if (self.num_imgs < self.pool_size):
            self.num_imgs = (self.num_imgs + 1)
            self.images.append(image)
            return_images.append(image)
        else:
            p = random.uniform(0, 1)
            if (p > 0.5):
                random_id = random.randint(0, (self.pool_size - 1))
                tmp = self.images[random_id].clone()
                self.images[random_id] = image
                return_images.append(tmp)
            else:
                return_images.append(image)
    return_images = torch.cat(return_images, 0)
    return return_images
