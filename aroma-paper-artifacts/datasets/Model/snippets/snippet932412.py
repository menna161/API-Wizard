from vue import *
from selenium.webdriver.common.by import By


def app(el):

    class CustomVModel(VueComponent):
        model = Model(prop='checked', event='change')
        checked: bool
        template = '\n            <div>\n                <p id="component">{{ checked }}</p>\n                <input\n                    id="c"\n                    type="checkbox"\n                    :checked="checked"\n                    @change="$emit(\'change\', $event.target.checked)"\n                >\n            </div>\n            '
    CustomVModel.register('custom-vmodel')

    class App(VueComponent):
        clicked = False
        template = '\n            <div>\n                <p id=\'instance\'>{{ clicked }}</p>\n                <custom-vmodel v-model="clicked"></custom-vmodel>\n            </div>\n            '
    return App(el)
