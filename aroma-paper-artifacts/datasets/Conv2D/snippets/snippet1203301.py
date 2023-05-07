import tinynn as tn


def conv_bn_relu(kernel):
    return [tn.layer.Conv2D(kernel=kernel, stride=(1, 1), padding='SAME'), tn.layer.ReLU()]
