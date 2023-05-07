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


def isolate_grid_table(self):
    messages = []
    blank_finish = 1
    try:
        block = self.state_machine.get_text_block(flush_left=True)
    except statemachine.UnexpectedIndentationError as err:
        (block, src, srcline) = err.args
        messages.append(self.reporter.error('Unexpected indentation.', source=src, line=srcline))
        blank_finish = 0
    block.disconnect()
    block.pad_double_width(self.double_width_pad_char)
    width = len(block[0].strip())
    for i in range(len(block)):
        block[i] = block[i].strip()
        if (block[i][0] not in '+|'):
            blank_finish = 0
            self.state_machine.previous_line((len(block) - i))
            del block[i:]
            break
    if (not self.grid_table_top_pat.match(block[(- 1)])):
        blank_finish = 0
        for i in range((len(block) - 2), 1, (- 1)):
            if self.grid_table_top_pat.match(block[i]):
                self.state_machine.previous_line(((len(block) - i) + 1))
                del block[(i + 1):]
                break
        else:
            messages.extend(self.malformed_table(block))
            return ([], messages, blank_finish)
    for i in range(len(block)):
        if ((len(block[i]) != width) or (block[i][(- 1)] not in '+|')):
            messages.extend(self.malformed_table(block))
            return ([], messages, blank_finish)
    return (block, messages, blank_finish)
