import logging
import datetime


def log_instantiation(LOGGER, classname, args, forbidden, with_date=False):
    '\n    Log the instantiation of an object to the given logger.\n\n    :LOGGER: A logger to log to. Please see module "logging".\n    :classname: The name of the class that is being\n        instantiated.\n    :args: A dictionary of arguments passed to the instantiation,\n        which will be logged on debug level.\n    :forbidden: A list of arguments whose values should not be\n        logged, e.g. "password".\n    :with_date: Optional. Boolean. Indicated whether the initiation\n        date and time should be logged.\n    '
    if with_date:
        LOGGER.info(((('Instantiating ' + classname) + ' at ') + datetime.datetime.now().strftime('%Y-%m-%d_%H:%M')))
    else:
        LOGGER.info(('Instantiating ' + classname))
    for argname in args:
        if (args[argname] is not None):
            if (argname in forbidden):
                LOGGER.debug((('Param ' + argname) + '*******'))
            else:
                LOGGER.debug(((('Param ' + argname) + '=') + str(args[argname])))
