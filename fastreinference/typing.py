# AUTOGENERATED! DO NOT EDIT! File to edit: 00_typing.ipynb (unless otherwise specified).

__all__ = ['Member', 'Mem', 'FunctionalEnum', 'DocumentedEnum', 'enumify']

# Cell
import enum
import inspect
import typing
from typing import Any
from functools import wraps, partial

# Cell
class _MemberGenericAlias(typing._GenericAlias, _root=True):
    def copy_with(self, params):
        return Member[params]

    def __eq__(self, other):
        if not isinstance(other, _MemberGenericAlias):
            return NotImplemented
        return set(self.__args__) == set(other.__args__)

    def __hash__(self):
        return hash(frozenset(self.__args__))

    def __repr__(self):
        args = list(self.__args__)
        if len(args) > 0:
            return f'Member[doc="{args[0]}"]'
        return f'Member[]'

    def __instancecheck__(self, obj):
        return self.__subclasscheck__(type(obj))

    def __reduce__(self):
        func, (origin, args) = super().__reduce__()
        return func, (Member, args)

    @property
    def doc(self):
        args = self.__args__
        if len(self.__args__) > 0:
            return args[0]
        return None

# Cell
@typing._SpecialForm
def Member(self, parameters):
    """Member type; Member[X] means documentation for the annotated item

    Used to quickly write documented Enums that may
    have a value of the member name, in lower case.

    To define a member type:
      - Member["Some documentation"]

    If there is an assign statement after the Member typing, the value for that enum member will be it.
    Otherwise it will be the member name, in lower case:
    ```python
    someValue:Member # Will be "somevalue"
    someThing:Member["My thing"] # Will have documentaiton of "My thing" and a value of "something"
    someThing:Member["My thing"] = 2 # Will have documentation of "My thing" and a value of 2

    The documentation can be accessed with `Member.doc`
    """
    if parameters == ():
        raise TypeError("Cannot take a Member without documentation")
    if not isinstance(parameters, (tuple, list)):
        parameters = (parameters,)
    if len(parameters) > 1:
        raise ValueError(f'Member was passed more than a single value ({len(parameters)}). Please only pass in a docstring: {parameters}')
    return _MemberGenericAlias(self, parameters)

# Cell
@typing._SpecialForm
def Mem(self, parameters):
    "Shorthand version of `Member`"
    return Member[parameters]

# Cell
class FunctionalEnum(enum.Enum):
    """
    An `Enum` class implementing `__ne__`, `__eq__`, and `__str__` to compare `self.value`.

    Compatible with the functional API.
    """
    def __str__(self): return str(self.value)
    def __eq__(self, other): return getattr(other, "value", other) == self.value
    def __ne__(self, other): return getattr(other, "value", other) != self.value

# Cell
class DocumentedEnum(FunctionalEnum):
    """
    An `Enum` capabile of having its members have docstrings.

    Inherits `FunctionalEnum` to allow for logic comparison via `==`, `!=`,
    and string representation `str()` of `self.value`
    """
    def __init__(self, *args):
        """
        Creates a generic enumeration with assigning of a member docstring

        Should be passed in the form of:
          docstring, value
        """
        if args[0] is not None:
            self.__doc__ = args[0]
        if len(args) > 1:
            self._value_ = args[1]
        else:
            self._value_ = None

# Cell
def _assign_annotations(cls):
    """
    Creates a `DocumentedEnum` based on annotations and asserts in `cls`
    """
    # First, filter out all but what we need: the doc, annotations, and any set members
    d = dict(cls.__dict__)
    _keep = ["__doc__", "__annotations__"]
    for key in list(d):
        if key.startswith('_') and key not in _keep:
            d.pop(key, None)
    names = [] # Names for our enum
    keys = []
    # Next get our members with out values
    for name, typ in list(d["__annotations__"].items()):
        if not (typ == Member or typ == Mem) and "Member[" not in str(typ):
            continue
        doc = getattr(typ, "doc", "An enumeration.")
        value = d.get(name, name.lower())
        names.append([name, (doc, value)])
        keys.append(name)

    # For any values set like a regular enum
    for name in d:
        if name not in keys and not name.startswith("_"):
            names.append([name, ("An enumeration.", getattr(cls, name))])
            keys.append(name)
    new_cls = DocumentedEnum(value=cls.__name__, names=names)
    new_cls.__doc__ = cls.__doc__
    return new_cls

# Cell
def enumify(cls=None):
    """
    A decorator to turn `cls` into an Enum class with member values as property names, and potentially with documentation

    Should be documented with the `Member` type with the following annotation:
    ```python
    from .typing import Member
    @enumify
    class MyClass:
      NAME:Member["Some documented enum value"]
      name_two:Member # An undocumented enum value
      name_three:Member["Some documentation"] = "some value"
    ```

    Can also use the shorthand `Mem` type
    """
    def wrap(cls): return _assign_annotations(cls)
    if cls is None:
        return partial(enumify)
    return wrap(cls)