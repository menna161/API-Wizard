import tinynn as tn


def D_cnn():
    return tn.net.Net([tn.layer.Conv2D(kernel=[5, 5, 1, 6], stride=[1, 1], padding='SAME'), tn.layer.LeakyReLU(), tn.layer.MaxPool2D(pool_size=[2, 2], stride=[2, 2]), tn.layer.Conv2D(kernel=[5, 5, 6, 16], stride=[1, 1], padding='SAME'), tn.layer.LeakyReLU(), tn.layer.MaxPool2D(pool_size=[2, 2], stride=[2, 2]), tn.layer.Flatten(), tn.layer.Dense(120), tn.layer.LeakyReLU(), tn.layer.Dense(84), tn.layer.LeakyReLU(), tn.layer.Dense(1)])
