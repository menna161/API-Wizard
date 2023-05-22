from copy import copy
from typing import Dict, List, Optional, Set, Tuple, cast
from grimp.algorithms.shortest_path import bidirectional_shortest_path
from grimp.application.ports import graph
from grimp.domain.valueobjects import Module
from grimp.exceptions import ModuleNotPresent


def find_shortest_chains(self, importer: str, imported: str) -> Set[Tuple[(str, ...)]]:
    '\n        Find the shortest import chains that exist between the importer and imported, and\n        between any modules contained within them. Only one chain per upstream/downstream pair\n        will be included. Any chains that are contained within other chains in the result set\n        will be excluded.\n\n        Returns:\n            A set of tuples of strings. Each tuple is ordered from importer to imported modules.\n        '
    shortest_chains = set()
    upstream_modules = self._all_modules_in_package(imported)
    downstream_modules = self._all_modules_in_package(importer)
    if (upstream_modules & downstream_modules):
        raise ValueError('Modules have shared descendants.')
    imports_between_modules = (self._find_all_imports_between_modules(upstream_modules) | self._find_all_imports_between_modules(downstream_modules))
    self._hide_any_existing_imports(imports_between_modules)
    map_of_imports = {}
    for module in (upstream_modules | downstream_modules):
        map_of_imports[module] = (set(((m, module) for m in self.find_modules_that_directly_import(module))) | set(((module, m) for m in self.find_modules_directly_imported_by(module))))
    for imports in map_of_imports.values():
        self._hide_any_existing_imports(imports)
    for upstream in upstream_modules:
        imports_of_upstream_module = map_of_imports[upstream]
        self._reveal_imports(imports_of_upstream_module)
        for downstream in downstream_modules:
            imports_by_downstream_module = map_of_imports[downstream]
            self._reveal_imports(imports_by_downstream_module)
            shortest_chain = self._find_shortest_chain(imported=upstream, importer=downstream)
            if shortest_chain:
                shortest_chains.add(shortest_chain)
            self._hide_any_existing_imports(imports_by_downstream_module)
        self._hide_any_existing_imports(imports_of_upstream_module)
    for imports in map_of_imports.values():
        self._reveal_imports(imports)
    self._reveal_imports(imports_between_modules)
    return shortest_chains
