from dataclasses import dataclass

from automapper.mapper import _try_get_field_value


@dataclass
class TestClass:
    map_field: str


def test_try_get_field_value__if_in_custom_mapping():
    is_found, mapped_value = _try_get_field_value("field1", None, {"field1": 123})

    assert is_found
    assert mapped_value == 123


def test_try_get_field_value__if_origin_has_same_field_attr():
    is_found, mapped_value = _try_get_field_value(
        "map_field", TestClass("Hello world"), None
    )

    assert is_found
    assert mapped_value == "Hello world"


def test_try_get_field_value__if_origin_contains_same_field_as_item():
    is_found, mapped_value = _try_get_field_value(
        "map_field", {"map_field": "Hello world. Again"}, None
    )

    assert is_found
    assert mapped_value == "Hello world. Again"


def test_try_get_field_value__if_field_not_found():
    is_found, mapped_value = _try_get_field_value("field1", None, None)

    assert not is_found
    assert mapped_value is None
