import matplotlib.pyplot as plt
from matplotlib import font_manager


def plot(ts, interpolate='previous', figure_width=12, linewidth=1, marker='o', markersize=3, color='#222222', aspect_ratio=None, font=None):
    try:
        import matplotlib.pyplot as plt
        from matplotlib import font_manager
    except ImportError:
        msg = 'need to install matplotlib for `plot` function'
        raise ImportError(msg)
    if (font is None):
        available_fonts = set((f.name for f in font_manager.fontManager.ttflist))
        for font in FONTS:
            if (font in available_fonts):
                break
    if (aspect_ratio is None):
        try:
            n_unique_values = len(ts.distribution())
        except KeyError:
            n_unique_values = 0
        scaled = min(MAX_ASPECT_POINTS, (max(2, n_unique_values) - 2))
        aspect_ratio = (MIN_ASPECT_RATIO + ((MAX_ASPECT_RATIO - MIN_ASPECT_RATIO) * (scaled / MAX_ASPECT_POINTS)))
    try:
        drawstyle = INTERPOLATE_DRAWSTYLE[interpolate]
    except KeyError:
        raise ValueError("invalid value for interpolate='{}', must be in {}".format(interpolate, set(INTERPOLATE_DRAWSTYLE.keys())))
    with plt.style.context(PLOT_STYLE):
        (figure, axes) = plt.subplots(figsize=(figure_width, (aspect_ratio * figure_width)))
        items = ts.items()
        if items:
            (x, y) = zip(*items)
        else:
            (x, y) = ([], [])
        plot = axes.plot(x, y, linewidth=linewidth, drawstyle=drawstyle, marker=marker, markersize=markersize, color=color)
        axes.set_aspect((aspect_ratio / axes.get_data_ratio()))
        axes.xaxis.set_major_locator(plt.MaxNLocator(int((figure_width / 2))))
        if font:
            plt.xticks(fontname=font)
            plt.yticks(fontname=font)
    return (figure, axes)
