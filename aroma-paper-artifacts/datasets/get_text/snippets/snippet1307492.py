import sys
import re
from types import FunctionType, MethodType
from docutils import nodes, statemachine, utils
from docutils import ApplicationError, DataError
from docutils.statemachine import StateMachineWS, StateWS
from docutils.nodes import fully_normalize_name as normalize_name
from docutils.nodes import whitespace_normalize_name
import docutils.parsers.rst
from docutils.parsers.rst import directives, languages, tableparser, roles
from docutils.parsers.rst.languages import en as _fallback_language_module
from docutils.utils import escape2null, unescape, column_width
from docutils.utils import punctuation_chars, roman, urischemes
from docutils.utils import split_escaped_whitespace
from docutils.parsers.rst import convert_directive_function


def text(self, match, context, next_state):
    'Paragraph.'
    startline = (self.state_machine.abs_line_number() - 1)
    msg = None
    try:
        block = self.state_machine.get_text_block(flush_left=True)
    except statemachine.UnexpectedIndentationError as err:
        (block, src, srcline) = err.args
        msg = self.reporter.error('Unexpected indentation.', source=src, line=srcline)
    lines = (context + list(block))
    (paragraph, literalnext) = self.paragraph(lines, startline)
    self.parent += paragraph
    self.parent += msg
    if literalnext:
        try:
            self.state_machine.next_line()
        except EOFError:
            pass
        self.parent += self.literal_block()
    return ([], next_state, [])
