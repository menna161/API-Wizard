import cv2
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from PIL.ExifTags import TAGS, GPSTAGS


def put_date(file, date):
    base_img_cv2 = cv2.imread(file)
    base_img = Image.open(file).convert('RGBA')
    txt = Image.new('RGB', base_img.size, (0, 0, 0))
    draw = ImageDraw.Draw(txt)
    fnt = ImageFont.truetype('./Arial Black.ttf', size=int(((base_img.size[0] + base_img.size[1]) / 100)))
    (textw, texth) = draw.textsize(date, font=fnt)
    draw.text((((base_img.size[0] * 0.95) - textw), ((base_img.size[1] * 0.95) - texth)), date, font=fnt, fill=font_color)
    txt_array = np.array(txt)
    output_img = cv2.addWeighted(base_img_cv2, 1.0, txt_array, 1.0, 0)
    return output_img
