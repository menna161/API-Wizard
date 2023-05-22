


def draw_bs_pairs_linreg(x, y, size=1):
    'Perform pairs bootstrap for linear regression.'
    inds = np.arange(len(x))
    bs_slope_reps = np.empty(size)
    bs_intercept_reps = np.empty(size)
    for i in range(size):
        bs_inds = np.random.choice(inds, size=len(inds))
        (bs_x, bs_y) = (x[bs_inds], y[bs_inds])
        (bs_slope_reps[i], bs_intercept_reps[i]) = np.polyfit(bs_x, bs_y, 1)
    return (bs_slope_reps, bs_intercept_reps)
