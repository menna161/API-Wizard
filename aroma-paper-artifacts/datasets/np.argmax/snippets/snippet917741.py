import numpy as np
import SimpleITK as sitk


def swap_flip_dimensions(cosine_matrix, image, header=None):
    swap = np.argmax(abs(cosine_matrix), axis=0)
    flip = np.sum(cosine_matrix, axis=0)
    image = np.transpose(image, tuple(swap))
    image = image[tuple((slice(None, None, int(f)) for f in flip))]
    if (header is None):
        return image
    header['spacing'] = tuple((header['spacing'][s] for s in swap))
    header['direction'] = np.eye(3)
    return (image, header)
