from collections import OrderedDict
import functools
import urllib.parse
import warnings
import numpy as np
from matplotlib import cbook, dviread, font_manager, rcParams
from matplotlib.font_manager import FontProperties, get_font
from matplotlib.ft2font import KERNING_DEFAULT, LOAD_NO_HINTING, LOAD_TARGET_LIGHT
from matplotlib.mathtext import MathTextParser
from matplotlib.path import Path
from matplotlib.transforms import Affine2D
from matplotlib.texmanager import TexManager


def get_text_path(self, prop, s, ismath=False, usetex=False):
    '\n        Convert text *s* to path (a tuple of vertices and codes for\n        matplotlib.path.Path).\n\n        Parameters\n        ----------\n\n        prop : `matplotlib.font_manager.FontProperties` instance\n            The font properties for the text.\n\n        s : str\n            The text to be converted.\n\n        usetex : bool, optional\n            Whether to use tex rendering. Defaults to ``False``.\n\n        ismath : bool, optional\n            If True, use mathtext parser. Effective only if\n            ``usetex == False``.\n\n        Returns\n        -------\n\n        verts, codes : tuple of lists\n            *verts*  is a list of numpy arrays containing the x and y\n            coordinates of the vertices. *codes* is a list of path codes.\n\n        Examples\n        --------\n\n        Create a list of vertices and codes from a text, and create a `Path`\n        from those::\n\n            from matplotlib.path import Path\n            from matplotlib.textpath import TextToPath\n            from matplotlib.font_manager import FontProperties\n\n            fp = FontProperties(family="Humor Sans", style="italic")\n            verts, codes = TextToPath().get_text_path(fp, "ABC")\n            path = Path(verts, codes, closed=False)\n\n        Also see `TextPath` for a more direct way to create a path from a text.\n        '
    if (not usetex):
        if (not ismath):
            font = self._get_font(prop)
            (glyph_info, glyph_map, rects) = self.get_glyphs_with_font(font, s)
        else:
            (glyph_info, glyph_map, rects) = self.get_glyphs_mathtext(prop, s)
    else:
        (glyph_info, glyph_map, rects) = self.get_glyphs_tex(prop, s)
    (verts, codes) = ([], [])
    for (glyph_id, xposition, yposition, scale) in glyph_info:
        (verts1, codes1) = glyph_map[glyph_id]
        if len(verts1):
            verts1 = ((np.array(verts1) * scale) + [xposition, yposition])
            verts.extend(verts1)
            codes.extend(codes1)
    for (verts1, codes1) in rects:
        verts.extend(verts1)
        codes.extend(codes1)
    return (verts, codes)
