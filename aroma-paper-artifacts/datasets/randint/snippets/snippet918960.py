from random import randint
from PIL import Image, ImageDraw, ImageFont


def get_random_color():
    return (randint(120, 200), randint(120, 200), randint(120, 200))
