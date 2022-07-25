from typing import List
from unittest import TestCase

import pytest
from pydantic import BaseModel

from automapper import mapper as default_mapper, Mapper, MappingError


class UserInfo(BaseModel):
    id: int
    full_name: str
    public_name: str
    hobbies: List[str]


class PublicUserInfo(BaseModel):
    id: int
    public_name: str
    hobbies: List[str]


class PydanticExtensionTest(TestCase):
    """These scenario are known for FastAPI Framework models and Pydantic models in general."""

    def setUp(self) -> None:
        self.mapper = Mapper()

    def test_map__fails_for_pydantic_mapping(self):
        obj = UserInfo(
            id=2,
            full_name="Danny DeVito",
            public_name="dannyd",
            hobbies=["acting", "comedy", "swimming"],
        )
        with pytest.raises(MappingError):
            self.mapper.to(PublicUserInfo).map(obj)

    def test_map__global_mapper_works_with_provided_pydantic_extension(self):
        obj = UserInfo(
            id=2,
            full_name="Danny DeVito",
            public_name="dannyd",
            hobbies=["acting", "comedy", "swimming"],
        )

        result = default_mapper.to(PublicUserInfo).map(obj)

        assert result.id == 2
        assert result.public_name == "dannyd"
        assert set(result.hobbies) == set(["acting", "comedy", "swimming"])
        with pytest.raises(AttributeError):
            getattr(result, "full_name")
