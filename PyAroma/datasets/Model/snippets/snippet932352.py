from unittest import mock
from vue import *


def test_customize_model():

    class Component(VueComponent):
        model = Model(prop='prop', event='event')
    init_dict = Component.init_dict()
    assert ({'prop': 'prop', 'event': 'event'} == init_dict['model'])
