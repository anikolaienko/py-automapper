from dataclasses import dataclass

import pytest

from automapper import mapper

@dataclass
class User:
    name: str
    age: int
    profession: str


@dataclass
class InputData:
    user: User


@dataclass
class OutputData:
    user: User
    username: str
    profession: str


def test_map__when_add_path_to_source_child_obj_field_with_diff_name__map_to_target():
    mapper.add(InputData, OutputData, {"username": mapper.path("user.name")})
    
    user = User("Mario", "25", "plumber")
    input = InputData(user)

    result: OutputData = mapper.map(input)

    assert result.username == user.name

def test_map__when_add_path_to_source_child_obj_field_with_same_name__map_to_target_field_implicitly():
    mapper.add(InputData, OutputData, {"profession": mapper.path("user.")})

    user = User("Mario", "25", "plumber")
    input = InputData(user)

    result: OutputData = mapper.map(input)

    assert result.profession 

def test_map__when_add_path_to_source_child_obj_field_with_wrong_type__raises_exception():
    with pytest.raises():
        mapper.add(InputData, OutputData, {"profession": mapper.path("user")})


def test_map__when_register_without_expr__map_string_literal():
    mapper.add(SourceCls, TargetCls, {"profession": "$.user.profession"})

    assert False

# def test_map__when_register_expr_without_dollar_sign__map_string_literal():
#     # We don't want to produce unexpected behaviour, sometimes the string just starts with $
#     mapper.add(SourceCls, TargetCls, {"profession": "$.user.profession"})

#     assert False

# def test_map__when_register_expr_to_target_child_obj__map_to_correctly():
#     mapper.add(SourceCls, TargetCls, {"user.profession": mapper.expr("$.profession")})
    
#     assert False

# def test_map__when_map_expr_to_source_child_obj_field__map_to_target():
#     mapper.to(TargetCls).map(source_obj, {"profession": mapper.expr("$.user.profession")})

#     assert False

# def test_map__when_map_expr_to_source_child_obj__map_to_target_field_implicitly():
#     mapper.to(TargetCls).map(source_obj, {"profession": mapper.expr("$.user")})

#     assert False

# def test_map__when_map_without_expr__map_string_literal():
#     mapper.to(TargetCls).map(source_obj, {"profession": "$.user.profession"})

#     assert False

# def test_map__when_map_expr_without_dollar_sign__map_string_literal():
#     # We don't want to produce unexpected behaviour, sometimes the string just starts with $
#     mapper.to(TargetCls).map(source_obj, {"profession": "$.user.profession"})

#     assert False

# def test_map__when_map_expr_to_target_child_obj__map_to_correctly():
#     mapper.to(TargetCls).map(source_obj, {"user.profession": mapper.expr("$.profession")})
    
#     assert False
