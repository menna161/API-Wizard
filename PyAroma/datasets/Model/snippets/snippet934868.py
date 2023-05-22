from .models import CoILICRA


def CoILModel(architecture_name, architecture_configuration):
    ' Factory function\n\n        Note: It is defined with the first letter as uppercase even though is a function to contrast\n        the actual use of this function that is making classes\n    '
    if (architecture_name == 'coil-icra'):
        return CoILICRA(architecture_configuration)
    else:
        raise ValueError(' Not found architecture name')
