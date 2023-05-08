import datetime
from datetime import timedelta
import pytest
from appkernel import ValidationException
from tests.utils import ExampleClass, Project, Task, Payment, PaymentMethod


def test_past_validation():
    project = Project().update(name='some project').append_to(tasks=Task().update(name='some task', description='some description'))
    project.tasks[0].complete()
    project.finalise_and_validate()
    print('{}'.format(project))
    project.tasks[0].update(closed_date=(datetime.datetime.now() - timedelta(days=1)))
    print('\n\n> one day in the past \n{}'.format(project))
    project.finalise_and_validate()
    with pytest.raises(ValidationException):
        project.tasks[0].update(closed_date=(datetime.datetime.now() + timedelta(days=1)))
        project.finalise_and_validate()
    with pytest.raises(ValidationException):
        project.tasks[0].update(closed_date='past')
        project.finalise_and_validate()
