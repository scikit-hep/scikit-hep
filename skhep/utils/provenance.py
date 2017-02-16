# Licensed under a 3-clause BSD style license, see LICENSE.

import json

from .py23 import *

# These are user-facing classes that structure the provenance information (history of operations performed on the dataset).

class Provenance(object):
    def __init__(self):
        raise TypeError("Provenance is an abstract base class; instantiate one of its subclasses instead.")

    @property
    def detail(self):
        """String providing more detail about the origin, transformation, or formatting."""
        raise NotImplementedError

class Origin(Provenance):
    # The first object in a provenance list.
    def __init__(self):
        raise TypeError("Origin is an abstract base class; instantiate one of its subclasses instead.")

class FileOrigin(Origin):
    # Declares that the dataset came from a file.
    def __init__(self, files):
        if isinstance(files, string_types):
            self.files = (files,)
        else:
            self.files = []
            for x in files:
                if isinstance(x, file):
                    self.files.append(x.name)
                elif isinstance(x, string_types):
                    self.files.append(x)
                else:
                    assert False, "files must be a string filename, an iterable of file objects, or an iterable of string filenames"
            self.files = tuple(self.files)

    @property
    def detail(self):
        return ", ".join(json.dumps(x) for x in self.files)

    def __repr__(self):
        return "<FileOrigin {0}>".format(self.detail)

class ObjectOrigin(Origin):
    # Declares that the dataset came from some Python object. Its history prior to that is unknown.
    def __init__(self, detail):
        self._detail = detail

    @property
    def detail(self):
        return self._detail

    def __repr__(self):
        return "<ObjectOrigin>"

class Transformation(Provenance):
    # Declares that the dataset was transformed by some mathematical operation.
    def __init__(self, name, args):
        self.name = name
        self.args = args

    @property
    def detail(self):
        return "{0}({1})".format(self.name, ", ".format(x.detail if isinstance(x, Provenance) else repr(x) for x in self.args))

    def __repr__(self):
        return "<{0}>".format(self.name)

class Formatting(Provenance):
    # Declares that the dataset was reformatted, keeping its semantic meaning, but changed in representation.
    def __init__(self, format, args):
        self.format = format
        self.args = args

    @property
    def detail(self):
        return "{0}({1})".format(self.format, ", ".format(x.detail if isinstance(x, Provenance) else repr(x) for x in self.args))
