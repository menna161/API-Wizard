import datetime
from datetime import timedelta
import pytest
from appkernel import ValidationException
from tests.utils import ExampleClass, Project, Task, Payment, PaymentMethod


def test_future_validation():
    test_model = ExampleClass()
    test_model.just_numbers = 123
    test_model.finalise_and_validate()
    test_model.future_field = (datetime.datetime.now() + timedelta(days=1))
    test_model.finalise_and_validate()
    with pytest.raises(ValidationException):
        test_model.future_field = (datetime.datetime.now() - timedelta(days=1))
        print('\n\n> one day in the in the future \n{}'.format(test_model))
        test_model.finalise_and_validate()
    with pytest.raises(ValidationException):
        test_model.future_field = 'future'
        test_model.finalise_and_validate()
