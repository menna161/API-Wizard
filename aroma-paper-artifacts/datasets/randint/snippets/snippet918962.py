from random import randint
from PIL import Image, ImageDraw, ImageFont


def generate_captcha(width=140, height=60, length=4):
    img = Image.new('RGB', (width, height), (250, 250, 250))
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype('static/font/font.ttf', size=36)
    text = ''
    for i in range(length):
        c = get_random_code()
        text += c
        rand_len = randint((- 5), 5)
        draw.text(((((width * 0.2) * (i + 1)) + rand_len), ((height * 0.2) + rand_len)), c, font=font, fill=get_random_color())
    for i in range(3):
        x1 = randint(0, width)
        y1 = randint(0, height)
        x2 = randint(0, width)
        y2 = randint(0, height)
        draw.line((x1, y1, x2, y2), fill=get_random_color())
    for i in range(16):
        draw.point((randint(0, width), randint(0, height)), fill=get_random_color())
    img.save((('static/captcha/' + text) + '.jpg'))
    return (text + '.jpg')
