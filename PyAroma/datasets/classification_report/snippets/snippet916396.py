from bs4 import BeautifulSoup, Comment
from django import template


@register.filter
def html_cleanup(text):
    doc = BeautifulSoup(text, 'html.parser')
    comments = doc.findAll(text=(lambda text: isinstance(text, Comment)))
    [comment.extract() for comment in comments]
    new_text = doc
    return new_text
