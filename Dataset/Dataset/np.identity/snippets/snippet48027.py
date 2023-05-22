import numpy as np
from .utils_img import bin2gray, bin2rgb
from .encoder import encode
from .decoder import get_message, decode
from .utils import check_random_state
import warnings


def decode_img(tG, H, codeword, snr, img_shape, maxiter=100):
    'Decode a received noisy image in the codeword.\n\n    Parameters\n    ----------\n    tG: array (n, k) coding matrix G\n    H: array (m, n) decoding matrix H\n    img_coded: array (n, n_blocks) image recieved in the codeword\n    snr: float. signal to noise ratio assumed of the channel.\n    img_shape: tuple of int. Shape of the original binary image.\n    maxiter: int. Max number of BP iterations to perform.\n    n_jobs: int. Number of parallel jobs.\n\n    Returns\n    -------\n    img_decode: array(width, height, depth). Decoded image.\n\n    '
    (n, k) = tG.shape
    (_, n_blocks) = codeword.shape
    depth = img_shape[(- 1)]
    if (depth not in [8, 24]):
        raise ValueError(('The expected dimension of a binary image is (width, height, 8) for grayscale images or (width, height, 24) for RGB images; got %s' % list(img_shape)))
    if (len(codeword) != n):
        raise ValueError('The left dimension of `codeword` must be equal to n, the number of columns of H.')
    systematic = True
    if (not (tG[(:k, :)] == np.identity(k)).all()):
        warnings.warn('In LDPC applications, using systematic coding matrix\n                         G is highly recommanded to speed up decoding.')
        systematic = False
    codeword_solution = decode(H, codeword, snr, maxiter)
    if systematic:
        decoded = codeword_solution[(:k, :)]
    else:
        decoded = np.array([get_message(tG, codeword_solution[(:, i)]) for i in range(n_blocks)]).T
    decoded = decoded.flatten()[:np.prod(img_shape)]
    decoded = decoded.reshape(*img_shape)
    if (depth == 8):
        decoded_img = bin2gray(decoded)
    else:
        decoded_img = bin2rgb(decoded)
    return decoded_img
