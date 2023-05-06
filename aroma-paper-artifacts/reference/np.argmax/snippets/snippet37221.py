import chainer
import chainer.functions as F
from chainer import initializers
import chainer.links as L
import numpy as np


def forward(self, x, t):
    h = self.bn1(self.conv1(x))
    h = F.max_pooling_2d(F.relu(h), 3, stride=2)
    h = self.res2(h)
    h = self.res3(h)
    h = self.res4(h)
    h = self.res5(h)
    h = F.average_pooling_2d(h, 7, stride=1)
    h = self.fc(h)
    loss = self.softmax_cross_entropy(h, t)
    if self.compute_accuracy:
        chainer.report({'loss': loss, 'accuracy': F.accuracy(h, np.argmax(t, axis=1))}, self)
    else:
        chainer.report({'loss': loss}, self)
    return loss
