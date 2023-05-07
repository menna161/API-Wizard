from random import randint
from PIL import Image, ImageDraw, ImageFont


def get_random_code():
    codes = [[chr(i) for i in range(48, 58)], [chr(i) for i in range(65, 91)], [chr(i) for i in range(97, 123)]]
    codes = codes[randint(0, 2)]
    return codes[randint(0, (len(codes) - 1))]
