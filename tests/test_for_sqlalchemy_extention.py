from unittest import TestCase

import pytest
from automapper import Mapper, MappingError
from automapper import mapper as default_mapper
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class UserInfo(Base):  # type: ignore[misc,valid-type]
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    full_name = Column(String)
    public_name = Column(String)
    hobbies = Column(String)

    def __repr__(self):
        return "<User(full_name='%s', public_name='%s', hobbies='%s')>" % (
            self.full_name,
            self.public_name,
            self.hobbies,
        )


class PublicUserInfo(Base):  # type: ignore[misc,valid-type]
    __tablename__ = "public_users"
    id = Column(Integer, primary_key=True)
    public_name = Column(String)
    hobbies = Column(String)


class SQLalchemyORMExtensionTest(TestCase):
    """These scenarios are known for ORM systems.
    e.g. Model classes in Tortoise ORM
    """

    def setUp(self) -> None:
        self.mapper = Mapper()

    def test_map__fails_for_sqlalchemy_mapping(self):
        obj = UserInfo(
            id=2,
            full_name="Danny DeVito",
            public_name="dannyd",
            hobbies="acting, comedy, swimming",
        )
        with pytest.raises(MappingError):
            self.mapper.to(PublicUserInfo).map(obj)

    def test_map__global_mapper_works_with_provided_sqlalchemy_extension(self):
        obj = UserInfo(
            id=2,
            full_name="Danny DeVito",
            public_name="dannyd",
            hobbies="acting, comedy, swimming",
        )

        result = default_mapper.to(PublicUserInfo).map(obj)

        assert result.id == 2
        assert result.public_name == "dannyd"
        assert result.hobbies == "acting, comedy, swimming"
        with pytest.raises(AttributeError):
            getattr(result, "full_name")
