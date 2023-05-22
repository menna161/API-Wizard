import FreeCAD, Part
import math
from functools import cmp_to_key
from pivy import coin
from itertools import groupby


def buildFaceCoordinates(brep):
    triangles = []
    faces = []
    groups = groupby(brep.coordIndex, (lambda coord: (coord == (- 1))))
    triangles = [tuple(group) for (k, group) in groups if (not k)]
    nextTriangle = 0
    for triangleCount in brep.partIndex:
        faces.append(triangles[nextTriangle:(nextTriangle + triangleCount)])
        nextTriangle += triangleCount
    return faces
