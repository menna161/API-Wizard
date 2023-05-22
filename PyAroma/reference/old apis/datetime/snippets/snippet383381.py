import datetime
from awe import CustomElement
from ..infra import element_tester, driver, page


def finder(driver):
    element = driver.find_element_by_class_name(custom_class)
    datetime.datetime.strptime(element.text[:19], '%Y-%m-%dT%H:%M:%S')
