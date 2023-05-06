import numpy as np
import warnings
from .utils_audio import bin2audio
from .encoder import encode
from .decoder import get_message, decode


def decode_audio(tG, H, codeword, snr, audio_shape, maxiter=1000):
    'Decode a received noisy audio file in the codeword.\n\n    Parameters\n    ----------\n    tG: array (n, k) coding matrix G\n    H: array (m, n) decoding matrix H\n    audio_coded: array (length n) audio in the codeword space\n    snr: float. signal to noise ratio assumed of the channel.\n    audio_shape: tuple (2,). Shape of original audio data.\n    maxiter: int. Max number of BP iterations to perform.\n\n    Returns\n    -------\n    audio_decoded: array (length,) original audio.\n\n    '
    (n, k) = tG.shape
    if (k != 17):
        raise ValueError('coding matrix G must have 17 rows\n                         (audio files are written in int16 which is\n                         equivalent to uint17)')
    (_, n_blocks) = codeword.shape
    systematic = True
    if (not (tG[(:k, :)] == np.identity(k)).all()):
        warnings.warn('In LDPC applications, using systematic coding matrix\n                         G is highly recommanded to speed up decode.')
        systematic = False
    codeword_solution = decode(H, codeword, snr, maxiter)
    if systematic:
        decoded = codeword_solution[(:k, :)]
    else:
        decoded = np.array([get_message(tG, codeword_solution[(:, i)]) for i in range(n_blocks)]).T
    decoded = decoded.flatten()[:np.prod(audio_shape)]
    decoded = decoded.reshape(*audio_shape)
    audio_decoded = bin2audio(decoded)
    return audio_decoded
