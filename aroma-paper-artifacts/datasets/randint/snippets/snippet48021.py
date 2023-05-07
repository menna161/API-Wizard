from . import utils


def encode_random_message(tG, snr, seed=None):
    'Encode a random message given a generating matrix tG and a SNR.\n\n    Parameters\n    ----------\n    tG: array or scipy.sparse.csr_matrix (m, k). Transposed coding matrix\n    obtained from `pyldpc.make_ldpc`.\n    snr: float. Signal-Noise Ratio. SNR = 10log(1 / variance) in decibels.\n\n    Returns\n    -------\n    v: array (k,) random message generated.\n    y: array (n,) coded message + noise.\n\n    '
    rng = utils.check_random_state(seed)
    (n, k) = tG.shape
    v = rng.randint(2, size=k)
    d = utils.binaryproduct(tG, v)
    x = ((- 1) ** d)
    sigma = (10 ** ((- snr) / 20))
    e = (rng.randn(n) * sigma)
    y = (x + e)
    return (v, y)
