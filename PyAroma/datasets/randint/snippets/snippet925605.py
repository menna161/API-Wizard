from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import collections
import functools
import random
from mathematics_dataset import example
from mathematics_dataset.modules import train_test_split
from mathematics_dataset.sample import number
from mathematics_dataset.util import composition
from mathematics_dataset.util import display
import six
import sympy


def time(is_train):
    'Questions for calculating start, end, or time differences.'
    context = composition.Context()
    start_minutes = random.randint(1, ((24 * 60) - 1))
    while True:
        duration_minutes = random.randint(1, ((12 * 60) - 1))
        if (train_test_split.is_train(duration_minutes) == is_train):
            break
    end_minutes = (start_minutes + duration_minutes)

    def format_12hr(minutes):
        'Format minutes from midnight in 12 hr format.'
        hours = ((minutes // 60) % 24)
        minutes %= 60
        am_pm = ('AM' if (hours < 12) else 'PM')
        hours = (((hours - 1) % 12) + 1)
        return '{}:{:02} {}'.format(hours, minutes, am_pm)
    start = format_12hr(start_minutes)
    end = format_12hr(end_minutes)
    which_question = random.randint(0, 3)
    if (which_question == 0):
        template = random.choice(['What is {duration} minutes before {end}?'])
        return example.Problem(question=example.question(context, template, duration=duration_minutes, end=end), answer=start)
    elif (which_question == 1):
        template = random.choice(['What is {duration} minutes after {start}?'])
        return example.Problem(question=example.question(context, template, duration=duration_minutes, start=start), answer=end)
    else:
        template = random.choice(['How many minutes are there between {start} and {end}?'])
        return example.Problem(question=example.question(context, template, start=start, end=end), answer=duration_minutes)
