from os import path as p
from sys import exit
from subprocess import call, check_call, CalledProcessError
from manager import Manager


@manager.arg('where', 'w', help='Modules to check')
@manager.command
def prettify(where=None):
    'Prettify code with black'
    extra = (where.split(' ') if where else DEF_WHERE)
    try:
        check_call((['black'] + extra))
    except CalledProcessError as err:
        exit(err.returncode)
