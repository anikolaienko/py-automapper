from unittest import TestCase

import pytest
from tortoise import Model, fields

from automapper import mapper as default_mapper, Mapper, MappingError


class UserInfo(Model):
    id = fields.IntField(pk=True)
    full_name = fields.TextField()
    public_name = fields.TextField()
    hobbies = fields.JSONField()


class PublicUserInfo(Model):
    id = fields.IntField(pk=True)
    public_name = fields.TextField()
    hobbies = fields.JSONField()


class TortoiseORMExtensionTest(TestCase):
    """These scenario are known for ORM systems.
    e.g. Model classes in Tortoise ORM
    """

    def setUp(self) -> None:
        self.mapper = Mapper()

    def test_map__fails_for_tortoise_mapping(self):
        obj = UserInfo(
            id=2,
            full_name="Danny DeVito",
            public_name="dannyd",
            hobbies=["acting", "comedy", "swimming"],
        )
        with pytest.raises(MappingError):
            self.mapper.to(PublicUserInfo).map(obj)

    def test_map__global_mapper_works_with_provided_tortoise_extension(self):
        obj = UserInfo(
            id=2,
            full_name="Danny DeVito",
            public_name="dannyd",
            hobbies=["acting", "comedy", "swimming"],
            using_db=True,
        )

        result = default_mapper.to(PublicUserInfo).map(obj)

        assert result.id == 2
        assert result.public_name == "dannyd"
        assert set(result.hobbies) == set(["acting", "comedy", "swimming"])
        with pytest.raises(AttributeError):
            getattr(result, "full_name")
