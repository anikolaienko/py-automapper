from typing import Protocol, Type, TypeVar, Iterable, cast
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
    def __init__(self, text: str) -> None:
        self.text = text

    @classmethod
    def fields(cls) -> Iterable[str]:
        return ["text"]


class FieldsClassProtocol(Protocol):
    def fields(self) -> Iterable[str]:
        ...


def custom_fields_extractor(concrete_class: Type[T]) -> Iterable[str]:
    fields = []
    for val_name, val_type in concrete_class.__init__.__annotations__.items():
        if val_name != "return":
            fields.append(val_name)
    return fields


def fields_fn_verifier(concrete_class: Type[T]) -> bool:
    return callable(getattr(concrete_class, "fields", None))


def fields_fn_extractor(concrete_class: Type[T]) -> Iterable[str]:
    return cast(FieldsClassProtocol, concrete_class).fields()


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
        assert ["text"] == mapper_internal.__FIELD_EXTRACTORS_WITH_VERIFIER__[fields_fn_verifier](
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
        pass

    def test_add__appends_class_to_class_mapping(self):
        with pytest.raises(mapper.MappingError):
            mapper.map(ChildClass)

        mapper.register_cls_extractor(AnotherClass, custom_fields_extractor)
        mapper.add(ChildClass, AnotherClass)
        result = mapper.map(ChildClass(10, "test_message", True))

        assert isinstance(result, AnotherClass)
        assert result.text == "test_message"

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
