import numpy as np
from scipy.sparse import csr_matrix
from . import utils


def coding_matrix(H, sparse=True):
    'Return the generating coding matrix G given the LDPC matrix H.\n\n    Parameters\n    ----------\n    H: array (n_equations, n_code). Parity check matrix of an LDPC code with\n        code length `n_code` and `n_equations` number of equations.\n    sparse: (boolean, default True): if `True`, scipy.sparse format is used\n        to speed up computation.\n\n    Returns\n    -------\n    G.T: array (n_bits, n_code). Transposed coding matrix.\n\n    '
    if (type(H) == csr_matrix):
        H = H.toarray()
    (n_equations, n_code) = H.shape
    (Href_colonnes, tQ) = utils.gaussjordan(H.T, 1)
    Href_diag = utils.gaussjordan(np.transpose(Href_colonnes))
    Q = tQ.T
    n_bits = (n_code - Href_diag.sum())
    Y = np.zeros(shape=(n_code, n_bits)).astype(int)
    Y[((n_code - n_bits):, :)] = np.identity(n_bits)
    if sparse:
        Q = csr_matrix(Q)
        Y = csr_matrix(Y)
    tG = utils.binaryproduct(Q, Y)
    return tG
