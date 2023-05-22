import random
import time
from pypinyin import pinyin, Style
from snownlp import SnowNLP


def model_modern():
    '创作现代诗'
    models = ['iii', 'iiii', 'iiii', 'nvviiii', 'yy', 'aa的nn', 'cc', 'nnvvoo', 'ppnn', 'qqnnaayy', 'aaaannaa', 'nnvvnn', 'iiiaa', 'cccc', 'nn，aa而aa', 'oo', 'vnn，vnn', 'iii', 'nnvviii', 'ssnnvvsss', 'iiy', 'iiiy', 'ssnnvvnn', 'iii', 'iii']
    line = input('为你写诗，君要几句呢？\n')
    while ((not line.isdigit()) or (int(line) >= 500)):
        line = input('请输入小于500数字：')
    model = ''
    for i in range(int(line)):
        model += models[random.randint(0, (len(models) - 1))]
        if (random.random() > 0.6):
            model += '，'
        elif (random.random() > 0.7):
            model += '。/'
        else:
            model += '/'
    output(get_poem(model))
