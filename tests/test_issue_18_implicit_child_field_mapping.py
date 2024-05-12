from dataclasses import dataclass
from typing import Optional

from automapper import mapper


@dataclass
class UserDomain:
    id: int
    name: str
    email: str


@dataclass
class TodoDomain:
    description: str
    user: UserDomain


@dataclass
class TodoModel:
    description: str
    user: UserDomain
    user_id: Optional[int] = None


def test_map__implicit_mapping_of_child_obj_field_to_parent_obj_field_not_supported():
    user = UserDomain(id=123, name="carlo", email="mail_carlo")
    todo = TodoDomain(description="todo_carlo", user=user)

    mapper.add(TodoDomain, TodoModel)
    todo_model: TodoModel = mapper.map(todo)

    # Implicit field mapping between parent and child objects is not supported
    # TodoDomain.user.user_id should not map to TodoModel.user_id implicitly
    assert todo_model.user_id is None

    # Workaround: use explicit mapping
    todo_model1: TodoModel = mapper.map(todo, fields_mapping={"user_id": todo.user.id})

    assert todo_model1.user_id == 123
