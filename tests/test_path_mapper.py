import pytest
from automapper import mapper
from automapper.path_mapper import (  # Replace 'your_module' with the actual module name
    MapPath,
)


class BasicUser:
    def __init__(self, name: str, city: str):
        self.name = name
        self.city = city

    def __repr__(self):
        return f"BasicUser(name={self.name}, city={self.city})"


class AdvancedUser:
    def __init__(self, user: BasicUser, job: str, salary: int):
        self.user = user
        self.job = job
        self.salary = salary


class TestMapPath:
    """Test suite for the MapPath class."""

    def test_valid_map_path(self):
        """Test that MapPath correctly splits a valid path."""
        path = MapPath("some.example.path")
        assert path.path == "some.example.path"
        assert path.attributes == ["example", "path"]  # obj_prefix is excluded
        assert path.obj_prefix == "some"  # obj_prefix is correctly assigned

    def test_invalid_map_path_missing_dot(self):
        """Test that MapPath raises ValueError for paths without a dot."""
        with pytest.raises(
            ValueError, match="Invalid path: 'singleword' does not contain '.'"
        ):
            MapPath("singleword")

    def test_callable_behavior(self):
        """Test that calling an instance returns the correct split attributes."""
        path = MapPath("one.two.three")
        assert path() == ["two", "three"]

    def test_repr(self):
        """Test that __repr__ returns the expected string representation."""
        path = MapPath("foo.bar")
        assert (
            repr(path) == "MapPath(['bar'])"
        )  # Only attributes are shown, excluding obj_prefix


class TestMappingObjectAttributes:
    def test_use_registered_mapping_with_map_path(self):
        try:
            mapper.add(
                AdvancedUser,
                BasicUser,
                fields_mapping={
                    "name": MapPath("AdvancedUser.user.name"),
                    "city": MapPath("AdvancedUser.user.city"),
                },
            )

            user = BasicUser(name="John Malkovich", city="USA")
            advanced_user = AdvancedUser(user=user, job="Engineer", salary=100)

            mapped_basic_user: BasicUser = mapper.map(advanced_user)

            assert mapped_basic_user.name == advanced_user.user.name
            assert mapped_basic_user.city == advanced_user.user.city
        finally:
            mapper._mappings.clear()

    def test_map_object_directly_without_adding_map_path_cant_be_resolved(self):
        """Mapping nested objects without adding registration rule should fail."""
        try:
            user = BasicUser(name="John Malkovich", city="USA")
            advanced_user = AdvancedUser(user=user, job="Engineer", salary=100)

            with pytest.raises(TypeError):
                mapper.to(BasicUser).map(advanced_user)
        finally:
            mapper._mappings.clear()
