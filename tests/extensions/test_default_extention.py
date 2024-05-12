from collections import namedtuple
from typing import Any, Iterable, Protocol, Type, TypeVar, cast, runtime_checkable
from unittest import TestCase

from automapper import Mapper
from automapper.extensions.default import extend

T = TypeVar("T")


class ClassWithoutInitAttrDef:
    def __init__(self, **kwargs: Any) -> None:
        self.data = kwargs.copy()

    @classmethod
    def fields(cls) -> Iterable[str]:
        return ["text", "num"]


@runtime_checkable
class ClassWithFieldsMethodProtocol(Protocol):
    def fields(self) -> Iterable[str]: ...


def classifier_func(target_cls: Type[T]) -> bool:
    return callable(getattr(target_cls, "fields", None))


def spec_func(target_cls: Type[T]) -> Iterable[str]:
    return cast(ClassWithFieldsMethodProtocol, target_cls).fields()


class DefaultExtensionTest(TestCase):
    def setUp(self):
        self.mapper = Mapper()
        extend(self.mapper)

    def test_default_extension__does_not_work_for_kwargs_in_init(self):
        obj = self.mapper.to(ClassWithoutInitAttrDef).map({"text": "text", "num": 1})
        assert len(obj.data) == 0

    def test_custom_spec_for_class__works_for_kwargs_in_init(self):
        self.mapper.add_spec(ClassWithoutInitAttrDef, spec_func)
        source = namedtuple("SourceObj", ["text", "num"])("text_msg", 11)  # type: ignore [call-arg]

        obj = self.mapper.to(ClassWithoutInitAttrDef).map(source)

        assert obj.data.get("text") == "text_msg"
        assert obj.data.get("num") == 11

    def test_custom_spec_with_classifier__works_for_kwargs_in_init(self):
        self.mapper.add_spec(classifier_func, spec_func)
        source = namedtuple("SourceObj", ["text", "num"])("text_msg", 11)  # type: ignore [call-arg]

        obj = self.mapper.to(ClassWithoutInitAttrDef).map(source)

        assert obj.data.get("text") == "text_msg"
        assert obj.data.get("num") == 11
