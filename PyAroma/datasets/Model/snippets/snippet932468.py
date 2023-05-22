from vue import *
from selenium.webdriver.common.by import By


def test_v_model(selenium):

    class VModel(VueComponent):
        clicked = False
        template = "<div>    <p id='p'>{{ clicked }}</p>    <input type='checkbox' id='c' v-model='clicked'></div>"
    with selenium.app(VModel):
        assert selenium.element_has_text('p', 'false')
        selenium.find_element(by=By.ID, value='c').click()
        assert selenium.element_has_text('p', 'true')
