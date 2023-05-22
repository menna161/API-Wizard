import abc
from typing import Iterator, List, Optional, Set, Tuple
from typing_extensions import TypedDict


def find_all_simple_chains(self, importer: str, imported: str) -> Iterator[Tuple[(str, ...)]]:
    '\n        Generate all simple chains between the importer and the imported modules.\n\n        Note: this method is no longer documented and will be removed.\n        '
    raise AttributeError('This method has been removed. Consider using find_shortest_chains instead?')
