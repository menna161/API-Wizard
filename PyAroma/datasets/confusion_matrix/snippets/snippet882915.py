import fasttext
import tools
from sklearn.metrics import precision_recall_fscore_support as score
from sklearn.metrics import confusion_matrix
import printcm
from tabulate import tabulate
import glob
import os
from collections import defaultdict


def run(fastTextModel, printErrors=False):
    model = FastTextTest(fastTextModel)
    data = readTestData(tools.config()['model']['test-file'])
    table = []
    all_truth = []
    all_prediction = []
    for row in data:
        (truth, prediction) = model.predict(row)
        result = stat_fscore(truth, prediction)
        table.append(([row[0]] + result))
        all_truth.extend(truth)
        all_prediction.extend(prediction)
    table.append((['all'] + stat_fscore(all_truth, all_prediction)))
    sumRow = ['sum']
    for col in range(1, len(table[0])):
        rowSum = sum(map((lambda x: x[col]), table))
        sumRow.append(rowSum)
    table.append(sumRow)
    headers = ['file', 'precisionMicro', 'recallMicro', 'fscoreMicro', 'precisionMacro', 'recallMacro', 'fscoreMacro']
    print(tabulate(table, headers, tablefmt='pipe', floatfmt='.4f'))
    title_description = 'FastText'
    plt = printcm.plot_confusion_matrix(all_truth, all_prediction, classes=['negative', 'neutral', 'positive'], normalize=True, title=title_description)
    plt.savefig('models/sentiment-cm.pdf')
    return table
