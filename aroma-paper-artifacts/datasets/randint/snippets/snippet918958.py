import os
import random
from flask import Flask, render_template


@app.route('/get_captcha', methods=['GET'])
def get_captcha():
    img_list = os.listdir('static/captcha')
    img = img_list[random.randint(0, 1000)]
    return os.path.join('static/captcha', img)
