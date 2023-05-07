import numpy as np
from chainer_bcnn.visualizer import ImageVisualizer
from chainer_bcnn.visualizer.image import _default_cmap


def test_classification():
    _categorical_cmaps = {'y': _default_cmap, 't': _default_cmap}
    _categorical_clims = {'x': (0.0, 1.0)}
    _categorical_transforms = {'x': (lambda x: x), 'y': (lambda x: np.argmax(x, axis=0)), 't': (lambda x: np.argmax(x, axis=0))}
    visualizer = ImageVisualizer(transforms=_categorical_transforms, cmaps=_categorical_cmaps, clims=_categorical_clims)
    x = np.random.rand(3, 100, 200)
    y = np.random.rand(10, 100, 200)
    t = np.random.rand(10, 100, 200)
    for _ in range(3):
        visualizer.add_example(x, y, t)
    visualizer.save('test_classification.png')