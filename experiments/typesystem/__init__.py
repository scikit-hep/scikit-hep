import sys

if sys.version_info[0] >= 3:
    long = int
    basestring = str
    xrange = range

# The name "schema" is used rather than "type" to avoid conflicts with Python's builtin.
class Schema(object):
    """The schema of a dataset describes the data type of its members."""

    def copy(self, classTable={}):
        raise NotImplementedError

    def supported(self):
        """In the top-level typesystem module, all types are supported."""
        return True

    def isinstance(self, datum):
        """In the top-level typesystem module, isinstance checks to see if a datum is a pure Python instance of the type (no Numpy, etc.)."""
        raise NotImplementedError
    
    def isdataset(self, data):
        """In the top-level typesystem module, isdataset checks to see if a dataset is a pure Python collection of the type (no Numpy, etc.)."""
        try:
            return all(self.isinstance(x) for x in data)
        except TypeError:
            return False

    def issubtype(self, schema):
        """supertype.issubtype(subtype) returns True; a member of subtype could be used where supertype is required."""
        return self._issubtype(schema, schema)

    def _issubtype(self, schema, top):
        raise NotImplementedError

    def dereference(self, *path):
        if len(path) == 0:
            return self
        else:
            raise TypeError("{0} cannot be dereferenced".format(self.__class__.__name__))

    def __repr__(self):
        return self.__class__.__name__ + "()"

    def __lt__(self, other):
        return self.order < other.order

    def __eq__(self, other):
        return self.__class__ == other.__class__

    def __hash__(self):
        return hash((self.__class__,))

class Anything(Schema):
    """Supertype of all other types, also known as the "top type."

    Useful for describing schemaless data like JSON."""
    order = 0
    def copy(self, classTable={}):
        return classTable.get("Anything", Anything)()
    def isinstance(self, datum):
        return True
    def _issubtype(self, schema, top):
        return True

class Nothing(Schema):
    """Type that has no members, also known as the "bottom type."

    Useful for describing the return type of exceptions and infinite loops."""
    order = 1
    def copy(self, classTable={}):
        return classTable.get("Nothing", Nothing)()
    def isinstance(self, datum):
        return False
    def _issubtype(self, schema, top):
        return isinstance(schema, Nothing)

class Null(Schema):
    """Type that has exactly one member, known variously as "null" or "None."

    Useful when combined with a union to make nullable data."""
    order = 2
    def copy(self, classTable={}):
        return classTable.get("Null", Null)()
    def isinstance(self, datum):
        return datum is None
    def _issubtype(self, schema, top):
        if isinstance(schema, Union) and len(schema.possibilities) == 1:
            return self._issubtype(schema.possibilities[0], top)
        return isinstance(schema, Null)

class Boolean(Schema):
    """Type that has exactly two members, known as "true" (or "True") and "false" (or "False").

    Useful for descring logical truth/falsehood, such as the predicate of a filter."""
    order = 3
    def copy(self, classTable={}):
        return classTable.get("Boolean", Boolean)()
    def isinstance(self, datum):
        return isinstance(datum, bool)
    def _issubtype(self, schema, top):
        if isinstance(schema, Union) and len(schema.possibilities) == 1:
            return self._issubtype(schema.possibilities[0], top)
        return isinstance(schema, Boolean)

class Number(Schema):
    """Type for describing all numbers, integral and floating-point.

    Has the following attributes:

       * whole: True for integral types, False for floating-point.
       * signed: True if negative values can be expressed, False otherwise.
       * nbytes: number of bytes: 4 for 32-bit int/float, 8 for 64-bit long/double."""

    order = 4

    def __init__(self, whole, signed, nbytes):
        self.whole = whole
        self.signed = signed
        self.nbytes = nbytes

    def copy(self, classTable={}):
        return classTable.get("Number", Number)(self.whole, self.signed, self.nbytes)

    def __repr__(self):
        return "{0}({1}, {2}, {3})".format(self.__class__.__name__, self.whole, self.signed, self.nbytes)

    def isinstance(self, datum):
        if self.signed or self.nbytes != 8:
            return False    # pure Python numbers are never unsigned or not 64-bit
        if self.whole:
            return isinstance(datum, (int, long))
        else:
            return isinstance(datum, (int, long, float))

    def _issubtype(self, schema, top):
        if isinstance(schema, Union) and len(schema.possibilities) == 1:
            return self._issubtype(schema.possibilities[0], top)
        if isinstance(schema, Number):
            if self.whole and not schema.whole:
                # self has no fractional values, but schema does
                return False
            if self.signed != schema.signed:
                # presence/absence of a sign bit changes the dynamic range in both directions
                return False
            if self.nbytes < schema.nbytes:
                # self has less dynamic range than schema
                return False
            # made it!
            return True
        else:
            return False

    def __lt__(self, other):
        if self.order == other.order:
            if self.whole == other.whole:
                if self.signed == other.signed:
                    return self.nbytes < other.nbytes
                else:
                    return self.signed < other.signed
            else:
                return self.whole < other.whole
        else:
            return self.order < other.order

    def __eq__(self, other):
        return self.__class__ == other.__class__ and self.whole == other.whole and self.signed == other.signed and self.nbytes == other.nbytes

    def __hash__(self):
        return hash((self.__class__, self.whole, self.signed, self.nbytes))

class String(Schema):
    """Type for describing strings of "characters," which may be uninterpreted individual bytes or variable-width Unicode sequences.

    Because of the possibility of variable-width items and the fact that humans think of strings differently from arrays of bytes, this is not a subclass of collection.

    Has the following attributes:

       * charset: "bytes", "utf-8", etc.
       * maxlength: None or a non-negative integer."""

    order = 5

    def __init__(self, charset, maxlength):
        self.charset = charset
        self.maxlength = maxlength

    def copy(self, classTable={}):
        return classTable.get("String", String)(self.charset, self.maxlength)

    def __repr__(self):
        return "{0}(\"{1}\", {2})".format(self.__class__.__name__, self.charset, self.maxlength)

    def supported(self):
        if self.charset not in ("bytes", "utf-8"):
            return False
        if self.maxlength is not None and self.maxlength < 0:
            return False
        # made it!
        return True

    def isinstance(self, datum):
        ok = False
        if sys.version_info[0] >= 3:
            if self.charset == "bytes" and isinstance(datum, bytes):
                ok = True
            if self.charset == "utf-8" and isinstance(datum, str):
                ok = True
        else:
            if self.charset == "bytes" and isinstance(datum, str):
                ok = True
            if self.charset == "utf-8" and isinstance(datum, unicode):
                ok = True
        if ok and self.maxlength is not None:
            ok = len(datum) <= self.maxlength
        return ok

    def _issubtype(self, schema, top):
        if isinstance(schema, Union) and len(schema.possibilities) == 1:
            return self._issubtype(schema.possibilities[0], top)
        if isinstance(schema, String):
            if self.charset != schema.charset:
                # different charset => no compatibility
                return False
            if self.maxlength is not None:
                if schema.maxlength is None:
                    # self has a maximum length but schema does not
                    return False
                if schema.maxlength > self.maxlength:
                    # both have maximum lengths, but schema's is longer
                    return False
            # made it!
            return True
        else:
            return False

    def __lt__(self, other):
        if self.order == other.order:
            if self.charset == other.charset:
                return (-1 if self.maxlength is None else self.maxlength) < (-1 if other.maxlength is None else other.maxlength)
            else:
                return self.charset < other.charset
        else:
            return self.order < other.order

    def __eq__(self, other):
        return self.__class__ == other.__class__ and self.charset == other.charset and self.maxlength == other.maxlength

    def __hash__(self):
        return hash((self.__class__, self.charset, self.maxlength))

class Tensor(Schema):
    """Array of some type (not necessarily numbers) with fixed dimensions.

    Has the following attributes:

       * items: schema of items contained in the tensor.
       * dimensions: tuple of positive integers (one for vector, two for matrix, etc.)."""
    
    order = 6

    def __init__(self, items, *dimensions):
        self.items = items
        self.dimensions = dimensions

    def copy(self, classTable={}):
        return classTable.get("Tensor", Tensor)(self.items.copy(classTable), *self.dimensions)

    def __repr__(self):
        return "{0}({1}, {2})".format(self.__class__.__name__, self.items, ", ".join(map(repr, self.dimensions)))

    def supported(self):
        if len(self.dimensions) < 1:
            return False
        else:
            return self.items.supported()

    def isinstance(self, datum):
        def check(dat, dim):
            if not isinstance(dat, (list, tuple)):
                # pure Python lists and tuples can be Tensors; ignore general iterables
                return False
            if len(dat) != dim[0]:
                # dimensions must match exactly
                return False
            # recursively check all subcomponents until the end of the dimensions list
            nextdim = dim[1:]
            if len(nextdim) == 0:
                return all(self.items.isinstance(nextdat) for nextdat in dat)
            else:
                return all(check(nextdat, nextdim) for nextdat in dat)
        return check(datum, self.dimensions)

    def _issubtype(self, schema, top):
        if isinstance(schema, Union) and len(schema.possibilities) == 1:
            return self._issubtype(schema.possibilities[0], top)
        if isinstance(schema, Tensor):
            if self.dimensions != schema.dimensions:
                # dimensions must match exactly
                return False
            if not self.items._issubtype(schema.items, top):
                # Tensors are covariant (e.g. int[3] is a subtype of float[3])
                return False
            # made it!
            return True
        else:
            return False

    def dereference(self, *path):
        def deref(ps, ds):
            t = Tensor(self.items, *ds)
            if len(ps) == 0:
                return t
            elif isinstance(ps[0], (int, long)):
                if ps[0] < ds[0]:
                    if len(ds) == 1:
                        return self.items.dereference(*ps[1:])
                    else:
                        return deref(ps[1:], ds[1:])
                else:
                    raise TypeError("can't dereference index {0} from tensor dimension {1}".format(ps[0], ds[0]))
            else:
                raise TypeError("can't use string {0} to dereference a tensor".format(ps[0]))

        return deref(path, self.dimensions)

    def __lt__(self, other):
        if self.order == other.order:
            if self.items == other.items:
                return self.dimensions < other.dimensions
            else:
                return self.items < other.items
        else:
            return self.order < other.order

    def __eq__(self, other):
        return self.__class__ == other.__class__ and self.items == other.items and self.dimensions == other.dimensions

    def __hash__(self):
        return hash((self.__class__, self.items, self.dimensions))

class Collection(Schema):
    """List or multiset of some type with variable dimension.

    Has the following attributes:

       * items: schema of items contained in the collection.
       * ordered: True if the collection has a meaningful order, False otherwise.
       * maxlength: None or a non-negative integer."""
    
    order = 7

    def __init__(self, items, ordered, maxlength):
        self.items = items
        self.ordered = ordered
        self.maxlength = maxlength

    def copy(self, classTable={}):
        return classTable.get("Collection", Collection)(self.items.copy(classTable), self.ordered, self.maxlength)

    def __repr__(self):
        return "{0}({1}, {2}, {3})".format(self.__class__.__name__, self.items, self.ordered, self.maxlength)

    def supported(self):
        if self.maxlength is not None and self.maxlength < 0:
            return False
        else:
            return self.items.supported()

    def isinstance(self, datum):
        if not isinstance(datum, (list, tuple, set)):
            # pure Python lists, tuples, and sets can be Collections; ignore general iterables
            return False
        # ignore ordered; we allow Python lists and tuples to be interpreted as unordered
        if self.maxlength is not None and len(datum) > self.maxlength:
            return False
        if not all(self.items.isinstance(dat) for dat in datum):
            return False
        # made it!
        return True

    def _issubtype(self, schema, top):
        if isinstance(schema, Union) and len(schema.possibilities) == 1:
            return self._issubtype(schema.possibilities[0], top)
        if isinstance(schema, Collection):
            if self.ordered and not schema.ordered:
                # ordered is a subtype of non-ordered
                return False
            if self.maxlength is not None:
                if schema.maxlength is None:
                    # self has a maximum length but schema does not
                    return False
                if schema.maxlength > self.maxlength:
                    # both have maximum lengths, but schema's is longer
                    return False
            if not self.items._issubtype(schema.items, top):
                # Collections are covariant (e.g. vector<int> is a subtype of vector<float>)
                return False
            # made it!
            return True
        else:
            return False

    def dereference(self, *path):
        if len(path) == 0:
            return self
        elif isinstance(path[0], (int, long)):
            if self.maxlength is None or path[0] < self.maxlength:
                if self.ordered:
                    return self.items.dereference(*path[1:])
                else:
                    raise TypeError("can't dereference index {0} from unordered collection".format(path[0]))
            else:
                raise TypeError("can't dereference index {0} from collection with maxlength {1}".format(path[0], self.maxlength))
        else:
            raise TypeError("can't use string {0} to dereference a collection".format(path[0]))

    def __lt__(self, other):
        if self.order == other.order:
            if self.items == other.items:
                if self.ordered == other.ordered:
                    return (-1 if self.maxlength is None else self.maxlength) < (-1 if schema.maxlength is None else schema.maxlength)
                else:
                    return self.ordered < other.ordered
            else:
                return self.items < other.items
        else:
            return self.order < other.order

    def __eq__(self, other):
        return self.__class__ == other.__class__ and self.items == other.items and self.ordered == other.ordered and self.maxlength == other.maxlength

    def __hash__(self):
        return hash((self.__class__, self.items, self.ordered, self.maxlength))

class Mapping(Schema):
    """Mapping/dictionary/associative array from keys to values.

    Has the following attributes:

       * keys: schema of the keys in the mapping.
       * values: schema of the values in the mapping."""

    order = 8

    def __init__(self, keys, values):
        self.keys = keys
        self.values = values

    def copy(self, classTable={}):
        return classTable.get("Mapping", Mapping)(self.keys.copy(classTable), self.values.copy(classTable))

    def __repr__(self):
        return "{0}({1}, {2})".format(self.__class__.__name__, self.keys, self.values)

    def supported(self):
        return self.keys.supported() and self.values.supported()

    def isinstance(self, datum):
        if not isinstance(datum, dict):
            return False
        if not all(self.keys.isinstance(dat) for dat in datum.keys()):
            return False
        if not all(self.values.isinstance(dat) for dat in datum.values()):
            return False
        # made it!
        return True

    def _issubtype(self, schema, top):
        if isinstance(schema, Union) and len(schema.possibilities) == 1:
            return self._issubtype(schema.possibilities[0], top)
        if isinstance(schema, Mapping):
            if not self.keys._issubtype(schema.keys, top):
                # Mappings are covariant in the keys
                return False
            if not self.values._issubtype(schema.values, top):
                # Mappings are covariant in the values
                return False
            # made it!
            return True
        else:
            return False

    def dereference(self, *path):
        if len(path) == 0:
            return self
        elif isinstance(self.keys, String) and isinstance(path[0], basestring):
            return self.values.dereference(*path[1:])
        elif isinstance(self.keys, Number) and self.keys.whole and isinstance(path[0], (int, long)):
            return self.values.dereference(*path[1:])
        else:
            raise TypeError("can't dereference mapping with key type {0} using {1} ({2})".format(self.keys, type(path[0]), path[0]))

    def __lt__(self, other):
        if self.order == other.order:
            if self.keys == other.keys:
                return self.values < other.values
            else:
                return self.keys < other.keys
        else:
            return self.order < other.order

    def __eq__(self, other):
        return self.__class__ == other.__class__ and self.keys == other.keys and self.values == other.values

    def __hash__(self):
        return hash((self.__class__, self.keys, self.values))
    
class Record(Schema):
    """Record/struct/class with a fixed set of named, typed fields. Also known as a "product type."

    Has the following attributes:

       * fields: dictionary from field names to schemas."""

    order = 9

    def __init__(self, **fields):
        self.fields = fields

    def copy(self, classTable={}):
        return classTable.get("Record", Record)(**dict((n, t.copy(classTable)) for n, t in self.fields.items()))

    def __repr__(self):
        return "{0}({1})".format(self.__class__.__name__, ", ".join(n + "=" + repr(t) for n, t in sorted(self.fields.items())))

    def supported(self):
        return all(t.supported() for t in self.fields.values())

    def isinstance(self, datum):
        # pure Python representation of a Record is a class instance
        for n, t in self.fields.items():
            if not hasattr(datum, n) or not t.isinstance(getattr(datum, n)):
                return False
        # made it!
        return True

    def _issubtype(self, schema, top):
        if isinstance(schema, Union) and len(schema.possibilities) == 1:
            return self._issubtype(schema.possibilities[0], top)
        if isinstance(schema, Record):
            # schema only needs to have the fields that self requires; it may have more
            for n, t in self.fields.items():
                if n not in schema.fields:
                    return False
                if not t._issubtype(schema.fields[n], top):
                    return False
            # made it!
            return True
        else:
            return False

    def dereference(self, *path):
        if len(path) == 0:
            return self
        elif isinstance(path[0], basestring):
            if path[0] in self.fields:
                return self.fields[path[0]].dereference(*path[1:])
            else:
                raise TypeError("can't dereference field named {0} from record".format(path[0]))
        else:
            raise TypeError("can't use int {0} to dereference a record".format(path[0]))

    def __lt__(self, other):
        if self.order == other.order:
            return sorted(self.fields.items()) < sorted(other.fields.items())
        else:
            return self.order < other.order

    def __eq__(self, other):
        return self.__class__ == other.__class__ and self.fields == other.fields

    def __hash__(self):
        return hash((self.__class__, tuple(sorted(self.fields.items()))))

class Union(Schema):
    """Tagged union of a set of types; a member may be an instance of any. Also known as a "sum type."

    Useful for describing nullable types (e.g. Union(Null(), String("utf-8", None))) and class hierarchies (e.g. union of all concrete classes in the hierarchy).

    Has the following attributes:

       * possibilities: sorted tuple of unique possibilities, flattening unions of unions."""

    order = 10

    def __init__(self, *possibilities):
        self.possibilities = []

        def insert(p):
            if isinstance(p, Union):
                for pp in p.possibilities:
                    # flatten unions of unions
                    insert(pp)
            else:
                # n**2 algorithm
                found = False
                for i, x in reversed(list(enumerate(self.possibilities))):
                    if x.issubtype(p):
                        # more general case is already in there
                        found = True
                    elif p.issubtype(x):
                        # p is more general; remove all subtypes
                        # indexing is not affected by removal because we're traversing backward
                        del self.possibilities[i]
                if not found:
                    self.possibilities.append(p)

        for p in possibilities:
            insert(p)

        self.possibilities = tuple(sorted(self.possibilities))

    def copy(self, classTable={}):
        return classTable.get("Union", Union)(*(p.copy(classTable) for p in self.possibilities))

    def __repr__(self):
        return "{0}({1})".format(self.__class__.__name__, ", ".join(map(repr, self.possibilities)))

    def supported(self):
        return all(t.supported() for t in self.possibilities)

    def isinstance(self, datum):
        for t in self.possibilities:
            if t.isinstance(datum):
                return True
        # made it!
        return False

    def _issubtype(self, schema, top):
        if isinstance(schema, Union) and len(schema.possibilities) == 1:
            return self._issubtype(schema.possibilities[0], top)
        if isinstance(schema, Union):
            # everything that a schema can be must also be allowed for self
            return all(any(t._issubtype(schemat, top) for t in self.possibilities) for schemat in schema.possibilities)
        else:
            return any(t._issubtype(schema, top) for t in self.possibilities)

    def dereference(self, *path):
        if len(path) == 0:
            return self
        else:
            raise TypeError("can't dereference a union type")

    def __lt__(self, other):
        if self.order == other.order:
            return self.possibilities < other.possibilities
        else:
            return self.order < other.order

    def __eq__(self, other):
        return self.__class__ == other.__class__ and self.possibilities == other.possibilities

    def __hash__(self):
        return hash((self.__class__, self.possibilities))

class Reference(Schema):
    """Index into another collection.

    Useful for representing pointers, cross-referencing data within an entry.

    Has the following attributes:

       * path: tuple of strings and integers pointing to an ordered collection."""

    order = 11

    def __init__(self, *path):
        self.path = path

    def copy(self, classTable={}):
        return classTable.get("Reference", Reference)(*self.path)

    def __repr__(self):
        return "{0}({1})".format(self.__class__.__name__, ", ".join(['"' + p + '"' if isinstance(p, basestring) else repr(p) for p in self.path]))

    def schema(self, top):
        return top.dereference(*(self.path + (0,)))

    def isinstance(self, datum):
        return isinstance(datum, (int, long))

    def _issubtype(self, schema, top):
        if isinstance(schema, Union) and len(schema.possibilities) == 1:
            return self._issubtype(schema.possibilities[0], top)
        return self.schema(top)._issubtype(schema, top)

    def dereference(self, *path):
        if len(path) == 0:
            return self
        else:
            raise TypeError("can't dereference a reference")

    def __lt__(self, other):
        if self.order == other.order:
            return self.path < other.path
        else:
            return self.order < other.order

    def __eq__(self, other):
        return self.__class__ == other.__class__ and self.path == other.path

    def __hash__(self):
        return hash((self.__class__, self.path))

def _pretty(schema, depth, comma):
    if isinstance(schema, (Anything, Nothing, Null, Boolean, Reference)):
        return [(depth, repr(schema) + comma, schema)]

    elif isinstance(schema, Number):
        return [(depth, "{0}(whole={1}, signed={2}, nbytes={3}){4}".format(schema.__class__.__name__, schema.whole, schema.signed, schema.nbytes, comma), schema)]

    elif isinstance(schema, String):
        return [(depth, "{0}(charset=\"{1}\", maxlength={2}){3}".format(schema.__class__.__name__, schema.charset, schema.maxlength, comma), schema)]

    elif isinstance(schema, Tensor):
        return [(depth, "{0}(".format(schema.__class__.__name__), schema)] + \
               _pretty(schema.items, depth + 1, ",") + \
               [(depth + 1, "{0}){1}".format(", ".join(map(repr, schema.dimensions)), comma), schema)]

    elif isinstance(schema, Collection):
        return [(depth, "{0}(".format(schema.__class__.__name__), schema)] + \
               _pretty(schema.items, depth + 1, ",") + \
               [(depth + 1, "ordered={0}, maxlength={1}){2}".format(schema.ordered, schema.maxlength, comma), schema)]

    elif isinstance(schema, Mapping):
        keys = _pretty(schema.keys, depth + 1, ",")
        keys = [(keys[0][0], "keys=" + keys[0][1], keys[0][2])] + keys[1:]

        values = _pretty(schema.values, depth + 1, "")
        values = [(values[0][0], "values=" + values[0][1], values[0][2])] + values[1:]

        return [(depth, "{0}(".format(schema.__class__.__name__), schema)] + \
                keys + values + \
               [(depth + 1, "){0}".format(comma), schema)]

    elif isinstance(schema, Record):
        fields = []
        for i, (n, t) in enumerate(sorted(schema.fields.items())):
            sub = _pretty(t, depth + 1, "," if i < len(schema.fields) - 1 else "")
            fields.extend([(sub[0][0], n + "=" + sub[0][1], sub[0][2])] + sub[1:])

        return [(depth, "{0}(".format(schema.__class__.__name__), schema)] + \
                fields + \
               [(depth + 1, "){0}".format(comma), schema)]

    elif isinstance(schema, Union):
        types = []
        for i, t in enumerate(schema.possibilities):
            sub = _pretty(t, depth + 1, "," if i < len(schema.possibilities) - 1 else "")
            types.extend(sub)

        return [(depth, "{0}(".format(schema.__class__.__name__), schema)] + \
                types + \
               [(depth + 1, "){0}".format(comma), schema)]

    else:
        raise Exception("shouldn't get here")

def pretty(schema, highlight=lambda t: ""):
    return "\n".join("{0}{1}{2}".format(highlight(subschema), "  " * depth, line) for depth, line, subschema in _pretty(schema, 0, ""))

def unsupported(schema):
    return pretty(schema, lambda t: "--> " if not t.supported() else "    ")

def compare(one, two, between=lambda t1, t2: " " if t1 == t2 or t1 is None or t2 is None else ">", width=None):
    one = _pretty(one, 0, "")
    two = _pretty(two, 0, "")
    i1 = 0
    i2 = 0
    if width is None:
        width = max(max([2*depth + len(line) for depth, line, _ in one]), max([2*depth + len(line) for depth, line, _ in two]))

    out = []
    while i1 < len(one) or i2 < len(two):
        d1, line1, t1 = one[i1] if i1 < len(one) else (d1, "", None)
        d2, line2, t2 = two[i2] if i2 < len(two) else (d2, "", None)

        if d1 >= d2:
            line1 = "  " * d1 + line1
            line1 = ("{:%d}" % width).format(line1[:width])
        if d2 >= d1:
            line2 = "  " * d2 + line2
            line2 = ("{:%d}" % width).format(line2[:width])
        
        if d1 == d2:
            out.append(line1 + " " + between(t1, t2) + " " + line2)
            i1 += 1
            i2 += 1
        elif d1 > d2:
            out.append(line1 + " " + between(t1, None) + " " + (" " * width))
            i1 += 1
        elif d2 > d1:
            out.append((" " * width) + " " + between(None, t2) + " " + line2)
            i2 += 1

    return "\n".join(out)
