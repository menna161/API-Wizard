from __future__ import print_function, division
from functools import wraps
from itertools import chain
from sympy.core import S
from sympy.core.compatibility import string_types, range
from sympy.core.decorators import deprecated
from sympy.codegen.ast import Assignment, Pointer, Variable, Declaration, real, complex_, integer, bool_, float32, float64, float80, complex64, complex128, intc, value_const, pointer_const, int8, int16, int32, int64, uint8, uint16, uint32, uint64, untyped
from sympy.printing.codeprinter import CodePrinter, requires
from sympy.printing.precedence import precedence, PRECEDENCE
from sympy.sets.fancysets import Range
from sympy.codegen.cfunctions import log2, Sqrt
from sympy.functions.elementary.exponential import log
from sympy.functions.elementary.miscellaneous import sqrt
from sympy.functions import Piecewise
from sympy.functions.elementary.trigonometric import sin
from sympy.core.relational import Ne
from sympy.functions import Piecewise
from sympy.codegen.cnodes import restrict


def get_math_macros():
    ' Returns a dictionary with math-related macros from math.h/cmath\n\n    Note that these macros are not strictly required by the C/C++-standard.\n    For MSVC they are enabled by defining "_USE_MATH_DEFINES" (preferably\n    via a compilation flag).\n\n    Returns\n    =======\n\n    Dictionary mapping sympy expressions to strings (macro names)\n\n    '
    from sympy.codegen.cfunctions import log2, Sqrt
    from sympy.functions.elementary.exponential import log
    from sympy.functions.elementary.miscellaneous import sqrt
    return {S.Exp1: 'M_E', log2(S.Exp1): 'M_LOG2E', (1 / log(2)): 'M_LOG2E', log(2): 'M_LN2', log(10): 'M_LN10', S.Pi: 'M_PI', (S.Pi / 2): 'M_PI_2', (S.Pi / 4): 'M_PI_4', (1 / S.Pi): 'M_1_PI', (2 / S.Pi): 'M_2_PI', (2 / sqrt(S.Pi)): 'M_2_SQRTPI', (2 / Sqrt(S.Pi)): 'M_2_SQRTPI', sqrt(2): 'M_SQRT2', Sqrt(2): 'M_SQRT2', (1 / sqrt(2)): 'M_SQRT1_2', (1 / Sqrt(2)): 'M_SQRT1_2'}
