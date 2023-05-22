from postmodel import models
import pytest
from postmodel.exceptions import OperationalError, ConfigurationError, PrimaryKeyChangedError
from tests.testmodels import MultiPrimaryFoo


def test_model_1():

    class NotModelClass():
        pass

    class Foo(models.Model):
        foo_id = models.IntField(pk=True)
        content = models.TextField()
    assert (Foo._meta != None)
    assert (len(Foo._meta.fields_map) == 2)

    class FooBar(Foo):
        bar_content = models.TextField()
    assert (len(FooBar._meta.fields_map) == 3)

    class ModelClassFromNotModel(NotModelClass, models.Model):
        id = models.AutoField()
        name = models.TextField()
    assert (ModelClassFromNotModel._meta != None)
    with pytest.raises(Exception):

        class DuplicatePKModel(ModelClassFromNotModel):
            dp_id = models.IntField(pk=True)
    with pytest.raises(Exception):

        class DuplicatedPrimaryKeyModel(models.Model):
            dp_id = models.IntField(pk=True)
            dp_no = models.AutoField()
