import datetime
from awe import CustomElement
from ..infra import element_tester, driver, page


def test_custom_element_external_script(element_tester):
    custom_class = 'custom1'

    class TestElement(CustomElement):
        _scripts = ['https://unpkg.com/moment@2.23.0/min/moment.min.js']

        @classmethod
        def _js(cls):
            return 'register((e) => <div {...e.props}>{moment().format()}</div>)'

    def builder(page):
        page.new(TestElement, props={'className': custom_class})

    def finder(driver):
        element = driver.find_element_by_class_name(custom_class)
        datetime.datetime.strptime(element.text[:19], '%Y-%m-%dT%H:%M:%S')
    element_tester(builder, finder)
