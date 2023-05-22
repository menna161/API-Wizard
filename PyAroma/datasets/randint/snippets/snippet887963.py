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


def get_verify_code(self):
    '\n        生成验证码图形\n        '
    code = ''.join(random.sample(string.digits, 4))
    for item in range(4):
        self.draw.text((((6 + random.randint((- 3), 3)) + (10 * item)), (2 + random.randint((- 2), 2))), text=code[item], fill=(random.randint(32, 127), random.randint(32, 127), random.randint(32, 127)), font=self.font)
    self.im = self.im.resize((100, 24))
    buffered = io.BytesIO()
    self.im.save(buffered, format='JPEG')
    img_str = (b'data:image/png;base64,' + base64.b64encode(buffered.getvalue()))
    return (img_str, code)
