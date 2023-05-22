import base64
import io
import random
import re
import string
from functools import wraps
import redis
from PIL import Image, ImageFont, ImageDraw
from flask import jsonify, current_app
from app.utils.response import ResMsg


def draw_lines(self, num=3):
    '\n        划线\n        '
    for num in range(num):
        x1 = random.randint(0, (self.width / 2))
        y1 = random.randint(0, (self.height / 2))
        x2 = random.randint(0, self.width)
        y2 = random.randint((self.height / 2), self.height)
        self.draw.line(((x1, y1), (x2, y2)), fill='black', width=1)
