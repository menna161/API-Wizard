import random
import time
from pypinyin import pinyin, Style
from snownlp import SnowNLP


def model_shi():
    '创作古诗'
    wujue = ['nnvss/nnvss/nnvvn/nnvvn/', 'nvnvn/nvnvn/nnvss/nnvss/']
    wulv = [('nnvvn/nnvvn/nnvvn/nnvvn/' * 2), ('nvnvn/nvnvn/nnvss/nnvss/' * 2)]
    qijue = ['nvnvnnv/nvnvnnv/nnvvnnv/nnvvnnv/', 'nvnnvvn/nvnnvvn/nnvvnns/nnvvnss/']
    qilv = [('nvnvnnv/nvnvnss/nnvvnnv/nnvvnss/' * 2), ('nvnnvvn/nvnnvvn/nnvvnnv/nnvvnss/' * 2)]
    tune_ = '0'
    while (tune_ not in ['1', '2', '3']):
        tune_ = input('需要平仄且押韵么？\n1.yao！切克闹 2.不为难你啦 3.不仅押，还要自定义韵脚！\n')
    tag = '0'
    while (tag not in ['1', '2', '3', '4']):
        tag = input('您需要什么格式：\n1.五言绝句 2.五言律诗 3.七言绝句 4.七言律诗\n')
    geshi = {'1': wujue, '2': wulv, '3': qijue, '4': qilv}
    model = geshi[tag][random.randrange((len(geshi[tag]) - 1))]
    if (tune_ == '2'):
        output(get_poem(plus_point(model)))
    elif (tune_ == '1'):
        (tune, yn) = get_tone(tag, yn=random.randint(0, 1))
        tune = tune.strip('/').split('/')
        model = model.strip('/').split('/')
        poem = ''
        for i in range(len(model)):
            foot_list = []
            foot = ''
            line = get_line_tone(model[i], tune[i])
            if (i == yn):
                foot = get_foot(line)
            count = 0
            while (((i % 2) == 1) and (rhyme(foot) != rhyme(get_foot(line))) and (count < 2000)):
                line = get_line_tone(model[i], tune[i])
                count += 1
            poem += (line + '/')
        poem = plus_point(poem)
        output(poem)
    else:
        word = input('请输字、词或句，将其尾韵作为韵脚:\n')
        while (not isChinese(word)):
            word = input('俺不认识这玩意儿，输入汉字哟：\n')
        foot = get_foot(word)
        model = model.strip('/').split('/')
        poem = ''
        for i in range(len(model)):
            line = get_poem(model[i])
            count = 0
            while (((i % 2) == 1) and (rhyme(foot) != rhyme(get_foot(line))) and (count < 2000)):
                line = get_poem(model[i])
                count += 1
            poem += (line + '/')
        poem = plus_point(poem)
        output(poem)
    return 0
