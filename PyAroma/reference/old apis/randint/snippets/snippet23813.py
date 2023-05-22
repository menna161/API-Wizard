import random
import time


def model_jing():
    models = ['nnvv，ssnn？/', 'ddnn，ssuu。/', 'uuss，nnss。/', 'aann，aann。/', 'vvuu，uuss。/', 'ssnn，vvuu。/', 'ssuu，iiii。/', 'iiii，nnss。/', 'ssuu，iiii。/', 'uuss，nnss。/', 'nnvv，ssnn。/', 'aann，aann。/', 'vvuu，uuss。/', 'ssnn，vvuu。/', 'ssuu，iiii。/', 'iiii，nnss。/', 'ssuu，iiii。/', 'uuss，nnss。/', 'nnvv，ssnn。/', 'aann，aann。/']
    model = ''
    for i in range(int(input('输入诗经行数，我可以无限创作哟！\n'))):
        model += models[random.randint(0, (len(models) - 1))]
    output(get_poem(model))
