from copy import copy
from typing import Dict, List, Optional, Set, Tuple, cast
from grimp.algorithms.shortest_path import bidirectional_shortest_path
from grimp.application.ports import graph
from grimp.domain.valueobjects import Module
from grimp.exceptions import ModuleNotPresent


def _find_all_imports_between_modules(self, modules: Set[str]) -> Set[Tuple[(str, str)]]:
    '\n        Return all the imports between the supplied set of modules.\n\n        Return:\n            Set of imports, in the form (importer, imported).\n        '
    imports = set()
    for importer in modules:
        for imported in self.find_modules_directly_imported_by(importer):
            if (imported in modules):
                imports.add((importer, imported))
    return imports
