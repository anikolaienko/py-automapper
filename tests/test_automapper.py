from typing import Protocol, Any, Type, TypeVar, Iterable, cast
from unittest import TestCase

import pytest

import automapper as mapper
import automapper.mapper as mapper_internal  # Used only for testing. Don't use it in client's code


# Test data
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

    @classmethod
    def fields(cls) -> Iterable[str]:
        return ["text", "num"]


class MetaClass(type):
    def __new__(mcs, name: str, bases: Any, attrs: dict):
        """Removes __annotations__ method from concrete class"""
        ...


class ClassWithoutAnnotations(metaclass=MetaClass):
    def __init__(self, **kwargs: Any) -> None:
        self.text = kwargs["text"]
        self.num = kwargs["num"]

    @classmethod
    def fields(cls) -> Iterable[str]:
        return ["text", "num"]


class ClassWithFieldsMethodProtocol(Protocol):
    def fields(self) -> Iterable[str]:
        ...


class ComplexClass:
    def __init__(self, obj: ParentClass, text: str) -> None:
        self.obj = obj
        self.text = text


class AnotherComplexClass:
    def __init__(self, text: str, obj: ChildClass) -> None:
        self.text = text
        self.obj = obj


def custom_fields_extractor(concrete_class: Type[T]) -> Iterable[str]:
    fields = []
    for val_name, val_type in concrete_class.__init__.__annotations__.items():
        if val_name != "return":
            fields.append(val_name)
    return fields


def fields_fn_verifier(target_cls: Type[T]) -> bool:
    return callable(getattr(target_cls, "fields", None))


def fields_fn_extractor(target_cls: Type[T]) -> Iterable[str]:
    return cast(ClassWithFieldsMethodProtocol, target_cls).fields()


# Test class
class AutomapperTest(TestCase):
    def setUp(self):
        self.initial_mappings = mapper_internal.__MAPPINGS__.copy()
        self.initial_field_extractors = mapper_internal.__FIELD_EXTRACTORS__.copy()
        self.initial_field_extractors_with_verifier = (
            mapper_internal.__FIELD_EXTRACTORS_WITH_VERIFIER__.copy()
        )

    def tearDown(self):
        mapper_internal.__MAPPINGS__ = self.initial_mappings
        mapper_internal.__FIELD_EXTRACTORS__ = self.initial_field_extractors
        mapper_internal.__FIELD_EXTRACTORS_WITH_VERIFIER__ = (
            self.initial_field_extractors_with_verifier
        )

    def test_register_cls_extractor__adds_to_internal_collection(self):
        mapper.register_cls_extractor(ParentClass, custom_fields_extractor)
        assert ParentClass in mapper_internal.__FIELD_EXTRACTORS__
        assert ["num", "text", "flag"] == mapper_internal.__FIELD_EXTRACTORS__[ParentClass](
            ChildClass
        )

    def test_register_cls_extractor__error_on_registering_same_class(self):
        mapper.register_cls_extractor(ParentClass, custom_fields_extractor)
        with pytest.raises(mapper.DuplicatedRegistration):
            mapper.register_cls_extractor(ParentClass, lambda concrete_type: ["field1", "field2"])

    def test_register_fn_extractor__adds_to_internal_collection(self):
        mapper.register_fn_extractor(fields_fn_verifier, fields_fn_extractor)
        assert fields_fn_verifier in mapper_internal.__FIELD_EXTRACTORS_WITH_VERIFIER__
        assert ["text", "num"] == mapper_internal.__FIELD_EXTRACTORS_WITH_VERIFIER__[fields_fn_verifier](
            AnotherClass
        )

    def test_register_fn_extractor__error_on_duplicated_registration(self):
        mapper.register_fn_extractor(fields_fn_verifier, fields_fn_extractor)
        with pytest.raises(mapper.DuplicatedRegistration):
            mapper.register_fn_extractor(
                fields_fn_verifier, lambda concrete_type: ["field1", "field2"]
            )

    def test__init_method_verifier__works_successfully(self):
        pass

    def test__init_method_verifier__does_not_cover_special_cases(self):
        obj = ChildClass(15, "sample", True)
        with pytest.raises(mapper.MappingError):
            mapper.to(ClassWithoutAnnotations).map(obj)

    def test_add__appends_class_to_class_mapping(self):
        with pytest.raises(mapper.MappingError):
            mapper.map(ChildClass)

        mapper.register_cls_extractor(AnotherClass, custom_fields_extractor)
        mapper.add(ChildClass, AnotherClass)
        result = mapper.map(ChildClass(10, "test_message", True))

        assert isinstance(result, AnotherClass)
        assert result.text == "test_message"
        assert result.num == 10

    def test_add__error_on_adding_same_source_class(self):
        class TempAnotherClass:
            pass

        mapper.add(ChildClass, AnotherClass)
        with pytest.raises(mapper.DuplicatedRegistration):
            mapper.add(ChildClass, TempAnotherClass)

    def test_to__produces_wrapper_for_mapping(self):
        source_obj = ChildClass(10, "test_text", False)

        result = mapper.to(AnotherClass).map(source_obj)

        assert isinstance(result, AnotherClass)
        assert result.text == "test_text"

    def test_map__skip_none_values_from_source_object(self):
        pass

    def test_map__pass_none_values_from_source_object(self):
        pass
