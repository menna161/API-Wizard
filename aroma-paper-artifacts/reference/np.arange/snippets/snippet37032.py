import os
import sys
import chainer
import numpy as np
import onnx
from test_case import TestCase
from chainer_compiler import ch2o


def _get_backprop_tests(dtype):
    chainer.config.dtype = dtype
    F = chainer.functions
    tests = []

    def test(name, model, *inputs, **kwargs):
        tests.append(BackpropTest(name, model, inputs, dtype, **kwargs))

    def aranges(*shape):
        r = np.prod(shape)
        return np.arange(r).reshape(shape).astype(np.float32)

    class Nop(chainer.Chain):

        def forward(self, x):
            return x
    test('nop', Nop(), aranges(2, 3))

    class AddSelf(chainer.Chain):

        def forward(self, x):
            return (x + x)
    test('add_self', AddSelf(), aranges(2, 3))

    class Linear(chainer.Chain):

        def __init__(self):
            super(Linear, self).__init__()
            with self.init_scope():
                self.l1 = L.Linear(None, 10)

        def forward(self, x):
            return F.relu(self.l1(x))
    test('linear', Linear(), aranges(2, 3))

    class LinearNoBias(chainer.Chain):

        def __init__(self):
            super(LinearNoBias, self).__init__()
            with self.init_scope():
                self.l1 = L.Linear(None, 10, nobias=True)

        def forward(self, x):
            return F.relu(self.l1(x))
    test('linear_nobias', LinearNoBias(), aranges(2, 3))

    class SoftmaxCrossEntropy(chainer.Chain):

        def __init__(self):
            super(SoftmaxCrossEntropy, self).__init__()
            with self.init_scope():
                self.l1 = L.Linear(None, 10)

        def forward(self, x, t):
            return F.softmax_cross_entropy(self.l1(x), t)
    test('softmax_cross_entropy', SoftmaxCrossEntropy(), aranges(2, 3), np.array([1, 0], dtype=np.int32))

    class LRN(chainer.Chain):

        def __init__(self):
            super(LRN, self).__init__()
            with self.init_scope():
                self.l1 = L.Linear(None, 10)

        def forward(self, x):
            return F.local_response_normalization(self.l1(x))
    test('lrn', LRN(), aranges(2, 3))

    class Stack(chainer.Chain):

        def __init__(self, axis):
            super(Stack, self).__init__()
            self.axis = axis
            with self.init_scope():
                self.l1 = L.Linear(None, 4)
                self.l2 = L.Linear(None, 4)

        def forward(self, x, y):
            xs = [(self.l1(x) * 2), (self.l2(y) * 3)]
            return F.stack(xs, axis=self.axis)
    test('stack', Stack(0), aranges(2, 3), (aranges(2, 3) + 1))
    test('stack_axis1', Stack(1), aranges(2, 3), (aranges(2, 3) + 1))

    class Concat(chainer.Chain):

        def __init__(self, axis):
            super(Concat, self).__init__()
            self.axis = axis
            with self.init_scope():
                self.l1 = L.Linear(None, 4)
                self.l2 = L.Linear(None, 4)

        def forward(self, x, y):
            xs = [(self.l1(x) * 2), (self.l2(y) * 3)]
            return F.concat(xs, axis=self.axis)
    test('concat', Concat(0), aranges(2, 3), (aranges(2, 3) + 1))
    test('concat_axis1', Concat(1), aranges(2, 3), (aranges(2, 3) + 1))

    class Separate(chainer.Chain):

        def __init__(self, axis):
            super(Separate, self).__init__()
            self.axis = axis
            with self.init_scope():
                self.l1 = L.Linear(None, 3)

        def forward(self, x):
            x = self.l1(x)
            xs = F.separate(x, axis=self.axis)
            return (((((xs[0] * xs[1]) * xs[1]) * xs[2]) * xs[2]) * xs[2])
    test('separate', Separate(0), aranges(3, 2))
    test('separate_axis1', Separate(1), aranges(3, 2))

    class Lookup(chainer.Chain):

        def __init__(self):
            super(Lookup, self).__init__()
            with self.init_scope():
                self.l1 = L.Linear(None, 4)
                self.l2 = L.Linear(None, 4)

        def forward(self, x, y, z):
            xs = [(self.l1(x) * 2), (self.l1(y) * 3), (self.l2(z) * 4)]
            return ((((((xs[0] * xs[2]) * xs[0]) * xs[1]) * xs[2]) * xs[2]) * xs[(- 1)])
    test('lookup', Lookup(), aranges(2, 3), (aranges(2, 3) + 1), (aranges(2, 3) + 2))

    class GetSlice(chainer.Chain):

        def __init__(self):
            super(GetSlice, self).__init__()
            with self.init_scope():
                self.l1 = L.Linear(None, 4)
                self.l2 = L.Linear(None, 4)

        def forward(self, x, y, z):
            xs = [(self.l1(x) * 2), (self.l1(y) * 3), (self.l2(z) * 4)]
            a = xs[0:2]
            b = xs[1:3]
            return (((a[0] * a[1]) * b[0]) * b[1])
    test('get_slice', GetSlice(), aranges(2, 3), (aranges(2, 3) + 1), (aranges(2, 3) + 2))

    class DynamicSlice(chainer.Chain):

        def __init__(self):
            super(DynamicSlice, self).__init__()
            with self.init_scope():
                self.l1 = L.Linear(None, 5)

        def forward(self, x):
            x = self.l1(x)
            a = x[1:3]
            b = x[2:4]
            return (a * b)
    test('dynamic_slice', DynamicSlice(), aranges(4, 2))

    class If(chainer.Chain):

        def __init__(self, cond):
            super(If, self).__init__()
            self.cond = cond
            with self.init_scope():
                self.l1 = L.Linear(None, 5)

        def forward(self, x):
            x = self.l1(x)
            if self.cond:
                x = (x * 3)
            else:
                x = (x * (- 2))
            return x
    test('if_true', If(True), aranges(4, 2))
    test('if_false', If(False), aranges(4, 2))

    class IfPartiallyDifferentiable(chainer.Chain):

        def __init__(self, cond):
            super(IfPartiallyDifferentiable, self).__init__()
            self.cond = cond
            with self.init_scope():
                self.l1 = L.Linear(None, 5)

        def forward(self, x):
            x = self.l1(x)
            y = 2
            if self.cond:
                x = (x * 3)
                y = 3
            else:
                x = (x * (- 2))
                y = 4
            return x[:y]
    test('if_pd_true', IfPartiallyDifferentiable(True), aranges(4, 2))
    test('if_pd_false', IfPartiallyDifferentiable(False), aranges(4, 2))

    class For(chainer.Chain):

        def __init__(self):
            super(For, self).__init__()
            with self.init_scope():
                self.l1 = L.Linear(4, 4)

        def forward(self, x):
            for _ in range(3):
                x = self.l1(x)
            return x
    test('for', For(), aranges(3, 4))

    class Embed(chainer.Chain):

        def __init__(self):
            super(Embed, self).__init__()
            with self.init_scope():
                self.emb = L.EmbedID(7, 4)

        def forward(self, x):
            return self.emb(x)
    test('embed', Embed(), np.array([3, 4, 5, 5, 5, 2]), skip_shape_inference=True)

    class Pad(chainer.Chain):

        def __init__(self):
            super(Pad, self).__init__()
            with self.init_scope():
                self.linear = L.Linear(None, 4)

        def forward(self, x):
            xs = F.separate(x)
            ys = []
            for x in xs:
                ys.append(self.linear(x))
            return F.pad_sequence(ys)
    test('pad', Pad(), aranges(5, 4, 3))
    return tests
