import time
import datetime
import requests
import re
from copy import deepcopy
import logging
import os
import pathlib
import traceback
import sys


@staticmethod
def save_to_file(dir_name, filename, content, audio=None, file_type=None, comments=None):
    '\n        将结果保存成文件的方法，保存在当前目录下\n        Args:\n            dir_name: 文件夹名称，如果不存在该文件夹则会创建文件夹\n            filename: 文件名称，直接新建\n            content: 需要保存的文本内容\n            audio: 需要填入文件中的音频文件（一般为音频地址）\n            file_type: 文档类型（需要保存什么类型的文档），默认保存为 Markdown 文档\n            comments: 评论相关数据\n        Returns:\n        '
    if (not file_type):
        file_type = '.md'
    dir_path = (pathlib.PurePosixPath() / dir_name)
    if (not os.path.isdir(dir_path)):
        os.mkdir(dir_path)
    filename = check_filename(filename)
    file_path = os.path.abspath((dir_path / (filename + file_type)))
    temp = ''
    if comments:
        with open('comment.css', 'r', encoding='utf-8') as f:
            comment_style = f.read()
        temp = (comment_style + '<ul>')
        for comment in comments:
            replie_str = ''
            for replie in comment.get('replies', []):
                replie_str += f"""<p class="_3KxQPN3V_0">{replie['user_name']}: {replie['content']}</p>"""
            comment_str = f'''<li>
<div class="_2sjJGcOH_0"><img src="{comment['user_header']}"
  class="_3FLYR4bF_0">
<div class="_36ChpWj4_0">
  <div class="_2zFoi7sd_0"><span>{comment['user_name']}</span>
  </div>
  <div class="_2_QraFYR_0">{comment['comment_content']}</div>
  <div class="_10o3OAxT_0">
    {replie_str}
  </div>
  <div class="_3klNVc4Z_0">
    <div class="_3Hkula0k_0">{datetime.datetime.fromtimestamp(comment['comment_ctime'])}</div>
  </div>
</div>
</div>
</li>
'''
            temp += comment_str
        temp += '</ul>'
    with open(file_path, 'w', encoding='utf-8') as f:
        if audio:
            audio_text = f'''<audio title="{filename}" src="{audio}" controls="controls"></audio> 
'''
            f.write(audio_text)
        f.write((content + temp))
