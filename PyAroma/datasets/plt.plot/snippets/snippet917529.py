import matplotlib as mpl
import matplotlib.pyplot as plt


def draw_predict_with_error(fig_id=None, data=None, error=None, filename=None, pathsave=None):
    plt.figure(fig_id)
    plt.plot(data[0])
    plt.plot(data[1])
    plt.ylabel('Real value')
    plt.xlabel('Point')
    plt.legend([('Predict y... RMSE= ' + str(error[0])), ('Test y... MAE= ' + str(error[1]))], loc='upper right')
    plt.savefig(((pathsave + filename) + '.png'))
    plt.close()
    return None
