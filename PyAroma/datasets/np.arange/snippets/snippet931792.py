


def draw_bs_pairs(x, y, func, size=1):
    'Perform pairs bootstrap for single statistic.'
    inds = np.arange(len(x))
    bs_replicates = np.empty(size)
    for i in range(size):
        bs_inds = np.random.choice(inds, len(inds))
        (bs_x, bs_y) = (x[bs_inds], y[bs_inds])
        bs_replicates[i] = func(bs_x, bs_y)
    return bs_replicates
