import base64
import os
import subprocess
import sys
import yaml


@classmethod
def remove_implicit_resolver(cls, tag_to_remove):
    "\n        Remove implicit resolvers for a particular tag\n\n        Takes care not to modify resolvers in super classes.\n\n        We want to load datetimes as strings, not dates, because we\n        go on to serialise as json which doesn't have the advanced types\n        of yaml, and leads to incompatibilities down the track.\n        "
    if ('yaml_implicit_resolvers' not in cls.__dict__):
        cls.yaml_implicit_resolvers = cls.yaml_implicit_resolvers.copy()
    for (first_letter, mappings) in cls.yaml_implicit_resolvers.items():
        cls.yaml_implicit_resolvers[first_letter] = [(tag, regexp) for (tag, regexp) in mappings if (tag != tag_to_remove)]
