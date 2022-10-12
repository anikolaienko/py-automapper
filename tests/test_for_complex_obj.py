from typing import Any, Iterable, Optional, Protocol, TypeVar
from unittest import TestCase

import pytest
from automapper import CircularReferenceError, create_mapper

T = TypeVar("T")


class ParentClass:
    def __init__(self, num: int, text: str) -> None:
        self.num = num
        self.text = text


class ChildClass(ParentClass):
    def __init__(self, num: int, text: str, flag: bool) -> None:
        super().__init__(num, text)
        self.flag = flag

    @classmethod
    def fields(cls) -> Iterable[str]:
        return (field for field in cls.__init__.__annotations__.keys() if field != "return")


class AnotherClass:
    def __init__(self, text: str, num: int) -> None:
        self.text = text
        self.num = num


class ClassWithoutInitAttrDef:
    def __init__(self, **kwargs: Any) -> None:
        self.data = kwargs.copy()

    @classmethod
    def fields(cls) -> Iterable[str]:
        return ["text", "num"]


class ClassWithFieldsMethodProtocol(Protocol):
    def fields(self) -> Iterable[str]:
        ...


class ComplexClass:
    def __init__(self, obj: ChildClass, text: str) -> None:
        self.obj = obj
        self.text = text


class AnotherComplexClass:
    def __init__(self, text: str, obj: ChildClass) -> None:
        self.text = text
        self.obj = obj


class ComplexObjWithCircularRef:
    def __init__(self, child: "WrapperClass"):
        self.child = child


class WrapperClass:
    def __init__(self, num: int, circular_ref_obj: Optional[ComplexObjWithCircularRef]):
        self.num = num
        self.circular_ref_obj = circular_ref_obj


class MappingComplexObjTest(TestCase):
    def setUp(self):
        self.mapper = create_mapper()

    def test_map__complext_obj(self):
        complex_obj = ComplexClass(obj=ChildClass(15, "nested_obj_msg", True), text="obj_msg")
        self.mapper.add(ChildClass, AnotherClass)
        self.mapper.add(ComplexClass, AnotherComplexClass)

        result: AnotherComplexClass = self.mapper.map(complex_obj)

        assert isinstance(result, AnotherComplexClass)
        assert isinstance(result.obj, AnotherClass)
        assert result.obj.text == "nested_obj_msg"
        assert result.obj.num == 15
        assert result.text == "obj_msg"

    def test_map__complext_obj_with_circular_ref(self):
        wrapper_obj = WrapperClass(15, None)
        source = ComplexObjWithCircularRef(wrapper_obj)

        self.mapper.add(ComplexObjWithCircularRef, ComplexObjWithCircularRef)
        self.mapper.add(WrapperClass, WrapperClass)

        result: ComplexObjWithCircularRef = self.mapper.map(source)
        assert result.child.num == 15

        # adding circular ref
        wrapper_obj.circular_ref_obj = source

        with pytest.raises(CircularReferenceError):
            result = self.mapper.map(source)
