from abc import abstractmethod
from unittest import TestCase
from typing import Any, Type, Iterable

import pytest

import automapper as mapper
import automapper.mapper as mapper_internal  # Used only for testing. Don't use it in client's code


class MetaClass(type):
    def __new__(mcs, name: str, bases: Any, attrs: dict):
        """Removes __annotations__ method from concrete class"""
        new_class = super().__new__(mcs, name, bases, attrs)
        delattr(new_class.__init__, "__annotations__")
        return new_class


class SourceClass:
    def __init__(self, num: int, text: str) -> None:
        self.num = num
        self.text = text


class BaseClass:
    @abstractmethod
    def fields(self):
        ...


class NoAnnotationsClass(metaclass=MetaClass):
    def __init__(self, **kwargs: Any) -> None:
        self.text = kwargs["text"]
        self.num = kwargs["num"]

    def fields(self):
        return ("text", "num")


def fields_cls_extractor(target_cls: Type[BaseClass]) -> Iterable[str]:
    return target_cls.fields()


class CustomExtractorTest(TestCase):
    """These scenario are known for ORM systems.
    e.g. Model classes in Tortoise ORM
    """

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

    def test_map__fails_for_no_annotations_class(self):
        obj = SourceClass(15, "This is a test text")
        with pytest.raises(mapper.MappingError):
            mapper.to(NoAnnotationsClass).map(obj)
    
    def test_map__works_with_provided_fields_extractor(self):
        mapper.register_cls_extractor(BaseClass, fields_cls_extractor)
        obj = SourceClass(17, "Test text")
        
        result = mapper.to(NoAnnotationsClass).map(SourceClass)

        assert result.num == 17
        assert result.text == "Test text"
