import re
from copy import deepcopy
import pytest
from grimp.adaptors.graph import ImportGraph
from grimp.exceptions import ModuleNotPresent


def test_removed_exception(self):
    with pytest.raises(AttributeError, match='This method has been removed. Consider using find_shortest_chains instead?'):
        ImportGraph().find_all_simple_chains(importer='foo', imported='bar')
