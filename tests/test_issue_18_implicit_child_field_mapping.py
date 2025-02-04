from dataclasses import dataclass
from typing import Optional

from automapper import mapper


@dataclass
class UserDomain:
    id: int
    name: str
    email: str


@dataclass
class InputDomain:
    description: str
    user: UserDomain


@dataclass
class OutputModel:
    description: str
    user: UserDomain
    user_id: Optional[int] = None


def test_map__implicit_mapping_of_child_obj_field_to_parent_obj_field_not_supported():
    user = UserDomain(id=123, name="carlo", email="mail_carlo")
    domain = InputDomain(description="todo_carlo", user=user)

    mapper.add(InputDomain, OutputModel)
    model_with_none_user_id: OutputModel = mapper.map(domain)

    # Implicit field mapping between parent and child objects is not supported
    # InputDomain.user.user_id should not map to OutputModel.user_id implicitly
    assert model_with_none_user_id.user_id is None

    # Workaround: use explicit mapping
    todo_model_complete: OutputModel = mapper.map(
        domain, fields_mapping={"user_id": domain.user.id}
    )

    assert todo_model_complete.user_id == 123
