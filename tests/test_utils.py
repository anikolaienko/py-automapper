from collections import OrderedDict
from enum import Enum

from automapper.utils import (
    is_dictionary,
    is_enum,
    is_primitive,
    is_sequence,
    is_subscriptable,
    object_contains,
)


def test_is_sequence__list_is_sequence():
    assert is_sequence([1, 2])


def test_is_sequence__tuple_is_sequence():
    assert is_sequence((1, 2, 3))


def test_is_sequence__dict_is_not_a_sequence():
    assert not is_sequence({"a": 1})


def test_is_dictionary__dict_is_of_type_dictionary():
    assert is_dictionary({"a1": 1})


def test_is_dictionary__ordered_dict_is_of_type_dictionary():
    assert is_dictionary(OrderedDict({"a1": 1}))


def test_is_subscriptable__dict_is_subscriptable():
    assert is_subscriptable({"a": 1})


def test_is_subscriptable__custom_class_can_be_subscriptable():
    class A:
        def __getitem__(self):
            yield 1

    assert is_subscriptable(A())


def test_object_contains__dict_contains_field():
    assert object_contains({"a1": 1, "b2": 2}, "a1")


def test_object_contains__dict_does_not_contain_field():
    assert not object_contains({"a1": 1, "b2": 2}, "c3")


def test_is_primitive__int_is_primitive():
    assert is_primitive(1)


def test_is_primitive__float_is_primitive():
    assert is_primitive(1.2)


def test_is_primitive__str_is_primitive():
    assert is_primitive("hello")


def test_is_primitive__bool_is_primitive():
    assert is_primitive(False)


def test_is_enum__object_is_enum():
    class EnumValue(Enum):
        A = "A"
        B = "B"

    assert is_enum(EnumValue("A"))


def test_is_enum__dict_is_not_enum():
    assert not is_enum({"A": 1, "B": 2})
