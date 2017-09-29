# Licensed under a 3-clause BSD style license, see LICENSE.
"""
Submodule for helpers to the Dataset-like classes
=================================================

User-facing classes that structure the provenance information, i.e. the history of operations performed on the dataset.

**Available classes:**

* ``Provenance`` (abstract base class).
* ``Origin`` (abstract base class).
* ``ObjectOrigin``.
* ``FileOrigin``.
* ``Transformation``.
* ``Formatting``.
"""

# -----------------------------------------------------------------------------
# Import statements
# -----------------------------------------------------------------------------
from __future__ import absolute_import

import json

from .exceptions import SkhepTypeError
from .py23 import *


# -----------------------------------------------------------------------------
# Provenance-like classes
# -----------------------------------------------------------------------------
class Provenance(object):
    """
    Abstract base class for all classes containing provenance information.

    Trying to instantiate it raises an exception. Instantiate one of its subclasses instead.
    """

    def __init__(self):
        raise SkhepTypeError('Provenance')

    @property
    def detail(self):
        """
        String providing detailed information about the origin, transformation, or formatting.
        """
        raise NotImplementedError


class Origin(Provenance):
    """
    Abstract base class for all classes describing the first object in a provenance list.

    Trying to instantiate it raises an exception. Instantiate one of its subclasses instead.
    """

    def __init__(self):
        raise SkhepTypeError('Origin')


class ObjectOrigin(Origin):
    """
    Declares that the dataset came from some Python object.
    Its history prior to that is unknown.

    :Parameters:
    detail: str
        String providing detailed information about the object origin.

    :Examples:
    >>> from skhep.utils import ObjectOrigin
    >>> from array import array
    >>> data = array('i',[1,2,3])
    >>> provenance1 = ObjectOrigin(repr(data))
    >>> provenance1
    <ObjectOrigin>
    >>> provenance1.detail
    "array('i', [1, 2, 3])"

    >>> provenance2 = ObjectOrigin('array_of_ints')
    >>> provenance2.detail
    'array_of_ints'
    """

    def __init__(self, detail):
        if not isinstance(detail, string_types):
            assert False, 'Argument is not of string type!'
        self._detail = detail

    @property
    def detail(self):
        return self._detail

    def __repr__(self):
        return "<ObjectOrigin>"


class FileOrigin(Origin):
    """
    Declares that the dataset came from a file or a set of files.

    :Parameters:
    files: str or iterable of str or file objects
        File name(s) or object(s).

    :Examples:
    >>> from skhep.utils import FileOrigin
    >>> prov = FileOrigin(['file1.root', 'file2.root','file3.root'])
    >>> prov
    <FileOrigin (3 files)>
    """

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
                    assert False, ('Argument must be a string filename, an iterable of file objects, '
                                   'or an iterable of string filenames!')
            self.files = tuple(self.files)

    @property
    def detail(self):
        return ", ".join(json.dumps(x) for x in self.files)

    def __repr__(self):
        return "<FileOrigin ({0} file{1})>".format(len(self.files),'s' if len(self.files)>1 else '')


class Transformation(Provenance):
    """
    Declares that the dataset was transformed by some mathematical operation.

    :Parameters:
    name: str
        String detailing how the dataset got transformed.
    args: iterable, optional
        Optional set of arguments given extra detail on the transformation.

    :Examples:
    >>> from skhep.utils import Transformation
    >>> transf = Transformation('all elms * 2')
    >>> transf
    <Transformation(all elms * 2)>
    """

    def __init__(self, name, args=[]):
        self.name = name
        self.args = args

    @property
    def detail(self):
        return "{0} ({1})".format(self.name,
                                 ", ".format(x.detail if isinstance(x, Provenance) else repr(x) for x in self.args))

    def __repr__(self):
        return "<Transformation({0})>".format(self.name)


class Formatting(Provenance):
    """
    Declares that the dataset was reformatted, keeping its semantic meaning, but changed in representation.
    """

    def __init__(self, format, args):
        self.format = format
        self.args = args

    @property
    def detail(self):
        return "{0}({1})".format(self.format,
                                 ", ".format(x.detail if isinstance(x, Provenance) else repr(x) for x in self.args))
