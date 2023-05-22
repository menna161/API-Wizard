from jinja2 import nodes
from jinja2.compiler import CodeGenerator
from jinja2._compat import string_types, iteritems


def find_referenced_templates(ast):
    'Finds all the referenced templates from the AST.  This will return an\n    iterator over all the hardcoded template extensions, inclusions and\n    imports.  If dynamic inheritance or inclusion is used, `None` will be\n    yielded.\n\n    >>> from jinja2 import Environment, meta\n    >>> env = Environment()\n    >>> ast = env.parse(\'{% extends "layout.html" %}{% include helper %}\')\n    >>> list(meta.find_referenced_templates(ast))\n    [\'layout.html\', None]\n\n    This function is useful for dependency tracking.  For example if you want\n    to rebuild parts of the website after a layout template has changed.\n    '
    for node in ast.find_all((nodes.Extends, nodes.FromImport, nodes.Import, nodes.Include)):
        if (not isinstance(node.template, nodes.Const)):
            if isinstance(node.template, (nodes.Tuple, nodes.List)):
                for template_name in node.template.items:
                    if isinstance(template_name, nodes.Const):
                        if isinstance(template_name.value, string_types):
                            (yield template_name.value)
                    else:
                        (yield None)
            else:
                (yield None)
            continue
        if isinstance(node.template.value, string_types):
            (yield node.template.value)
        elif (isinstance(node, nodes.Include) and isinstance(node.template.value, (tuple, list))):
            for template_name in node.template.value:
                if isinstance(template_name, string_types):
                    (yield template_name)
        else:
            (yield None)
