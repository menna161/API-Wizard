import copy
from . import model
from jsonschema.validators import validator_for


def model_factory(schema, base_class=model.Model, name=None, resolver=None):
    'Generate a model class based on the provided JSON Schema\n\n    :param schema: dict representing valid JSON schema\n    :param name: A name to give the class, if `name` is not in `schema`\n    '
    schema = copy.deepcopy(schema)
    resolver = resolver

    class Model(base_class):

        def __init__(self, *args, **kwargs):
            self.__dict__['schema'] = schema
            self.__dict__['resolver'] = resolver
            cls = validator_for(self.schema)
            if (resolver is not None):
                self.__dict__['validator_instance'] = cls(schema, resolver=resolver)
            else:
                self.__dict__['validator_instance'] = cls(schema)
            base_class.__init__(self, *args, **kwargs)
    if (resolver is not None):
        Model.resolver = resolver
    if (name is not None):
        Model.__name__ = name
    elif ('name' in schema):
        Model.__name__ = str(schema['name'])
    return Model
