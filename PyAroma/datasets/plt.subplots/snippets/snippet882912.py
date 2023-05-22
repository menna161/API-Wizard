import numpy as np
import matplotlib.pyplot as plt
import itertools
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from sklearn.utils.multiclass import unique_labels


def plot_confusion_matrix(y_true, y_pred, classes, normalize=False, title=None, cmap=None):
    '\n    This function prints and plots the confusion matrix.\n    Normalization can be applied by setting `normalize=True`.\n    '
    if (cmap is None):
        cmap = plt.get_cmap('Blues')
    if (not title):
        if normalize:
            title = 'Normalized confusion matrix'
        else:
            title = 'Confusion matrix, without normalization'
    cm = confusion_matrix(y_true, y_pred)
    if normalize:
        cm = (cm.astype('float') / cm.sum(axis=1)[(:, np.newaxis)])
        print('Normalized confusion matrix')
    else:
        print('Confusion matrix, without normalization')
    print(cm)
    (fig, ax) = plt.subplots()
    im = ax.imshow(cm, interpolation='nearest', cmap=cmap)
    ax.figure.colorbar(im, ax=ax)
    ax.set(xticks=np.arange(cm.shape[1]), yticks=np.arange(cm.shape[0]), xticklabels=classes, yticklabels=classes, title=title, ylabel='True label', xlabel='Predicted label')
    plt.setp(ax.get_xticklabels(), rotation=45, ha='right', rotation_mode='anchor')
    fmt = ('.2f' if normalize else 'd')
    thresh = (cm.max() / 2.0)
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            ax.text(j, i, format(cm[(i, j)], fmt), ha='center', va='center', color=('white' if (cm[(i, j)] > thresh) else 'black'))
    fig.tight_layout()
    plt.gcf().subplots_adjust(left=(- 0.05))
    return plt
