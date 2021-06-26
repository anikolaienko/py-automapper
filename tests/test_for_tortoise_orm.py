from dataclasses import dataclass
from unittest import TestCase

import pytest
from tortoise import Model, fields

from automapper import mapper as global_mapper, Mapper, MappingError


@dataclass
class SourceClass:
    id: int
    name: str
    

class TargetModel(Model):
    id = fields.IntField(pk=True)
    name = fields.TextField()


class TestsForTortoiseORM(TestCase):
    """These scenario are known for ORM systems.
    e.g. Model classes in Tortoise ORM
    """

    def setUp(self) -> None:
        self.mapper = Mapper()

    def test_map__fails_for_tortoise_mapping(self):
        obj = SourceClass(15, "This is a test text")
        with pytest.raises(MappingError):
            self.mapper.to(TargetModel).map(obj)

    def test_map__global_mapper_works_with_provided_extension(self):
        obj = SourceClass(17, "Test obj name")
        
        result = global_mapper.to(TargetModel).map(obj)

        assert result.id == 17
        assert result.name == "Test obj name"
