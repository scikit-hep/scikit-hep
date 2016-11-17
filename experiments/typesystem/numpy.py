import numpy

import typesystem

class NumpySchema(typesystem.Schema): pass

class Anything(NumpySchema, typesystem.Anything):
    def supported(self):
        return False
    def isinstance(self, datum):
        return False
    def isdataset(self, data):
        return False

class Nothing(NumpySchema, typesystem.Nothing):
    def supported(self):
        return False
    def isinstance(self, datum):
        return False
    def isdataset(self, data):
        return False

class Null(NumpySchema, typesystem.Null):
    def supported(self):
        return False
    def isinstance(self, datum):
        return False
    def isdataset(self, data):
        return False

class Boolean(NumpySchema, typesystem.Boolean):
    def supported(self):
        return True
    def isinstance(self, datum):
        return isinstance(datum, numpy.bool_)
    def isdataset(self, data):
        if isinstance(data, numpy.ndarray):
            return issubclass(data.dtype.type, numpy.bool_)
        else:
            return False

class Number(NumpySchema, typesystem.Number):
    def supported(self):
        if not self.whole and not self.signed:
            return False
        if self.whole and self.nbytes not in (1, 2, 4, 8):
            return False
        if not self.whole and self.nbytes not in (2, 4, 8, 16):
            return False
        # made it!
        return True

    def isinstance(self, datum):
        ok = False
        if self.whole:
            if self.signed:
                ok = isinstance(datum, numpy.signedinteger)
            else:
                ok = isinstance(datum, numpy.unsignedinteger)
            if ok:
                ok = self.nbytes == datum.dtype.itemsize
        else:
            if self.signed:
                ok = isinstance(datum, numpy.floating)
            if ok:
                ok = ok and self.nbytes == datum.dtype.itemsize
        return ok

    def isdataset(self, data):
        if isinstance(data, numpy.ndarray):
            ok = False
            if self.whole:
                if self.signed:
                    ok = issubclass(data.dtype.type, numpy.signedinteger)
                else:
                    ok = issubclass(data.dtype.type, numpy.unsignedinteger)
                if ok:
                    ok = ok and self.nbytes == data.dtype.itemsize
            else:
                if self.signed:
                    ok = issubclass(data.dtype.type, numpy.floating)
                if ok:
                    ok = ok and self.nbytes == data.dtype.itemsize
            return ok
        else:
            return False

class String(NumpySchema, typesystem.String):
    def supported(self):
        if self.charset not in ("bytes", "utf-32le"):
            return False
        if self.maxlength is not None and self.maxlength < 0:
            return False
        # made it!
        return True

    def isinstance(self, datum):
        ok = False
        if self.charset == "bytes":
            ok = isinstance(datum, numpy.string_)
        if self.charset == "utf-32le":
            # Numpy uses utf-32le to encode Unicode (on a little-endian machine, at least)
            ok = isinstance(datum, numpy.unicode_)
        if ok and self.maxlength is not None:
            ok = ok and datum.dtype.itemsize <= self.maxlength
        return ok

    def isdataset(self, data):
        ok = False
        if self.charset == "bytes":
            ok = isinstance(data.dtype.type, numpy.string_)
        if self.charset == "utf-32le":
            ok = isinstance(data.dtype.type, numpy.unicode_)
        if ok and self.maxlength is not None:
            ok = ok and data.dtype.itemsize <= self.maxlength
        return ok

class Tensor(NumpySchema, typesystem.Tensor):
    def isinstance(self, datum):
        if isinstance(datum, numpy.ndarray) and len(datum.shape) >= len(self.dimensions) and datum.shape[:len(self.dimensions)] == self.dimensions:
            return self.items.isinstance(datum.__array__()[(0,) * len(self.dimensions)])
        else:
            return False

    def isdataset(self, data):
        if isinstance(datum, numpy.ndarray):
            return self.isinstance(data.__array__()[0])
        else:
            return False

class Collection(NumpySchema, typesystem.Collection):
    def isinstance(self, datum):
        if isinstance(datum, numpy.ndarray):
            if self.maxlength is not None and datum.__array__().shape[0] > self.maxlength:
                return False
            return self.items.isinstance(datum.__array__()[0])
        else:
            return False

    def isdataset(self, data):
        if isinstance(datum, numpy.ndarray):
            return self.isinstance(data.__array__()[0])
        else:
            return False

class Mapping(NumpySchema, typesystem.Mapping):
    def supported(self):
        return False
    def isinstance(self, datum):
        return False
    def isdataset(self, data):
        return False

class Record(NumpySchema, typesystem.Record):
    def supported(self):
        # records can only contain primitives (or Union(X) where X is a single primitive)
        return all((isinstance(t, (Boolean, Number, String)) or \
                   (isinstance(t, Union) and len(t.possibilities) == 1 and isinstance(t.possibilities[0], (Boolean, Number, String)))) and \
                   t.supported() for t in self.fields.values())

    def isinstance(self, datum):
        if isinstance(datum, numpy.core.records.record) and datum.dtype.names is not None and set(self.fields.keys()).issubset(set(datum.dtype.names)):
            for n, t in self.fields.items():
                if not t.isinstance(datum[n]):
                    return False
            # made it!
            return True
        else:
            return False

    def isdataset(self, data):
        if isinstance(data, numpy.ndarray) and data.dtype.names is not None and set(self.fields.keys()).issubset(set(data.dtype.names)):
            for n, t in self.fields.items():
                if not t.isdataset(data[n]):
                    return False
            # made it!
            return True
        else:
            return False

class Union(NumpySchema, typesystem.Union):
    def supported(self):
        if len(self.possibilities) == 1:
            # Union(X) is just X
            return True

        elif len(self.possibilities) == 2 and any(isinstance(x, Null) for x in self.possibilities):
            # support Union(Null(), X) for any X (i.e. "nullable X")
            subtype = [x for x in self.possibilities if not isinstance(x, Null)][0]
            return subtype.supported()

        else:
            # don't support any other cases
            return False

    def isinstance(self, datum):
        if len(self.possibilities) == 1:
            # Union(X) is just X
            return self.possibilities[0].isinstance(datum)

        elif len(self.possibilities) == 2 and any(isinstance(x, Null) for x in self.possibilities):
            # support Union(Null(), X) for any X (i.e. "nullable X")
            subtype = [x for x in self.possibilities if not isinstance(x, Null)][0]
            return isinstance(datum, numpy.ma.core.MaskedConstant) or subtype.isinstance(datum)

        else:
            # don't support any other cases
            return False

    def isdataset(self, data):
        if len(self.possibilities) == 1:
            # Union(X) is just X
            return self.possibilities[0].isdataset(data)

        elif len(self.possibilities) == 2 and any(isinstance(x, Null) for x in self.possibilities):
            # support Union(Null(), X) for any X (i.e. "nullable X")
            subtype = [x for x in self.possibilities if not isinstance(x, Null)][0]
            if isinstance(data, numpy.ma.MaskedArray):
                return subtype.isdataset(data.data)
            else:
                return False

        else:
            # don't support any other cases
            return False

class Reference(NumpySchema, typesystem.Reference):
    def supported(self):
        return False
    def isinstance(self, datum):
        return False
    def isdataset(self, data):
        return False

def toNumpySchema(schema):
    return schema.copy({
        "Anything": Anything,
        "Nothing": Nothing,
        "Null": Null,
        "Boolean": Boolean,
        "Number": Number,
        "String": String,
        "Tensor": Tensor,
        "Collection": Collection,
        "Mapping": Mapping,
        "Record": Record,
        "Union": Union,
        "Reference": Reference})
