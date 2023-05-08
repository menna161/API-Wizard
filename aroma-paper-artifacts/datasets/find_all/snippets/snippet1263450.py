import re
from jinja2 import nodes
from jinja2.defaults import BLOCK_START_STRING, BLOCK_END_STRING, VARIABLE_START_STRING, VARIABLE_END_STRING, COMMENT_START_STRING, COMMENT_END_STRING, LINE_STATEMENT_PREFIX, LINE_COMMENT_PREFIX, TRIM_BLOCKS, NEWLINE_SEQUENCE, KEEP_TRAILING_NEWLINE, LSTRIP_BLOCKS
from jinja2.environment import Environment
from jinja2.runtime import concat
from jinja2.exceptions import TemplateAssertionError, TemplateSyntaxError
from jinja2.utils import contextfunction, import_string, Markup
from jinja2._compat import with_metaclass, string_types, iteritems


def extract_from_ast(node, gettext_functions=GETTEXT_FUNCTIONS, babel_style=True):
    'Extract localizable strings from the given template node.  Per\n    default this function returns matches in babel style that means non string\n    parameters as well as keyword arguments are returned as `None`.  This\n    allows Babel to figure out what you really meant if you are using\n    gettext functions that allow keyword arguments for placeholder expansion.\n    If you don\'t want that behavior set the `babel_style` parameter to `False`\n    which causes only strings to be returned and parameters are always stored\n    in tuples.  As a consequence invalid gettext calls (calls without a single\n    string parameter or string parameters after non-string parameters) are\n    skipped.\n\n    This example explains the behavior:\n\n    >>> from jinja2 import Environment\n    >>> env = Environment()\n    >>> node = env.parse(\'{{ (_("foo"), _(), ngettext("foo", "bar", 42)) }}\')\n    >>> list(extract_from_ast(node))\n    [(1, \'_\', \'foo\'), (1, \'_\', ()), (1, \'ngettext\', (\'foo\', \'bar\', None))]\n    >>> list(extract_from_ast(node, babel_style=False))\n    [(1, \'_\', (\'foo\',)), (1, \'ngettext\', (\'foo\', \'bar\'))]\n\n    For every string found this function yields a ``(lineno, function,\n    message)`` tuple, where:\n\n    * ``lineno`` is the number of the line on which the string was found,\n    * ``function`` is the name of the ``gettext`` function used (if the\n      string was extracted from embedded Python code), and\n    *  ``message`` is the string itself (a ``unicode`` object, or a tuple\n       of ``unicode`` objects for functions with multiple string arguments).\n\n    This extraction function operates on the AST and is because of that unable\n    to extract any comments.  For comment support you have to use the babel\n    extraction interface or extract comments yourself.\n    '
    for node in node.find_all(nodes.Call):
        if ((not isinstance(node.node, nodes.Name)) or (node.node.name not in gettext_functions)):
            continue
        strings = []
        for arg in node.args:
            if (isinstance(arg, nodes.Const) and isinstance(arg.value, string_types)):
                strings.append(arg.value)
            else:
                strings.append(None)
        for arg in node.kwargs:
            strings.append(None)
        if (node.dyn_args is not None):
            strings.append(None)
        if (node.dyn_kwargs is not None):
            strings.append(None)
        if (not babel_style):
            strings = tuple((x for x in strings if (x is not None)))
            if (not strings):
                continue
        elif (len(strings) == 1):
            strings = strings[0]
        else:
            strings = tuple(strings)
        (yield (node.lineno, node.node.name, strings))
