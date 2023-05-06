import numpy as np
from scipy.sparse import csr_matrix
from . import utils


def coding_matrix_systematic(H, sparse=True):
    'Compute a coding matrix G in systematic format with an identity block.\n\n    Parameters\n    ----------\n    H: array (n_equations, n_code). Parity-check matrix.\n    sparse: (boolean, default True): if `True`, scipy.sparse is used\n    to speed up computation if n_code > 1000.\n\n    Returns\n    -------\n    H_new: (n_equations, n_code) array. Modified parity-check matrix given by a\n        permutation of the columns of the provided H.\n    G_systematic.T: Transposed Systematic Coding matrix associated to H_new.\n\n    '
    (n_equations, n_code) = H.shape
    if ((n_code > 1000) or sparse):
        sparse = True
    else:
        sparse = False
    P1 = np.identity(n_code, dtype=int)
    Hrowreduced = utils.gaussjordan(H)
    n_bits = (n_code - sum([a.any() for a in Hrowreduced]))
    while True:
        zeros = [i for i in range(min(n_equations, n_code)) if (not Hrowreduced[(i, i)])]
        if len(zeros):
            indice_colonne_a = min(zeros)
        else:
            break
        list_ones = [j for j in range((indice_colonne_a + 1), n_code) if Hrowreduced[(indice_colonne_a, j)]]
        if len(list_ones):
            indice_colonne_b = min(list_ones)
        else:
            break
        aux = Hrowreduced[(:, indice_colonne_a)].copy()
        Hrowreduced[(:, indice_colonne_a)] = Hrowreduced[(:, indice_colonne_b)]
        Hrowreduced[(:, indice_colonne_b)] = aux
        aux = P1[(:, indice_colonne_a)].copy()
        P1[(:, indice_colonne_a)] = P1[(:, indice_colonne_b)]
        P1[(:, indice_colonne_b)] = aux
    P1 = P1.T
    identity = list(range(n_code))
    sigma = (identity[(n_code - n_bits):] + identity[:(n_code - n_bits)])
    P2 = np.zeros(shape=(n_code, n_code), dtype=int)
    P2[(identity, sigma)] = np.ones(n_code)
    if sparse:
        P1 = csr_matrix(P1)
        P2 = csr_matrix(P2)
        H = csr_matrix(H)
    P = utils.binaryproduct(P2, P1)
    if sparse:
        P = csr_matrix(P)
    H_new = utils.binaryproduct(H, np.transpose(P))
    G_systematic = np.zeros((n_bits, n_code), dtype=int)
    G_systematic[(:, :n_bits)] = np.identity(n_bits)
    G_systematic[(:, n_bits:)] = Hrowreduced[(:(n_code - n_bits), (n_code - n_bits):)].T
    return (H_new, G_systematic.T)
