from enum import Enum
from typing import Any, Dict, Sequence

__PRIMITIVE_TYPES = {int, float, complex, str, bytes, bytearray, bool}


def is_sequence(obj: Any) -> bool:
    """Check if object implements `__iter__` method"""
    return isinstance(obj, Sequence)


def is_dictionary(obj: Any) -> bool:
    """Check is object is of type dictionary"""
    return isinstance(obj, Dict)


def is_subscriptable(obj: Any) -> bool:
    """Check if object implements `__getitem__` method"""
    return hasattr(obj, "__getitem__")


def object_contains(obj: Any, field_name: str) -> bool:
    return is_subscriptable(obj) and field_name in obj


def is_primitive(obj: Any) -> bool:
    """Check if object type is primitive"""
    return type(obj) in __PRIMITIVE_TYPES


def is_enum(obj: Any) -> bool:
    """Check if object type is enum"""
    return issubclass(type(obj), Enum)
