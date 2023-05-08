import random
import time
from pypinyin import pinyin, Style
from snownlp import SnowNLP


def rd(typ, lenth):
    '按照词性和词长随机匹配最佳的词'
    ci = ''
    if (lenth > longest[typ]):
        ci = (rd(typ, 2) + rd(typ, (lenth - 2)))
    elif (lenth == 1):
        rand = random.randint(0, (len(typ_dict[typ]) - 1))
        ci = typ_dict[typ][rand]
        ci = ci[random.randrange(len(ci))]
    else:
        count = 0
        while (len(ci) != lenth):
            rand = random.randint(0, (len(typ_dict[typ]) - 1))
            ci = typ_dict[typ][rand]
            count += 1
    return ci
