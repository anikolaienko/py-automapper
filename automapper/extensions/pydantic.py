from typing import Iterable, Type

from automapper import Mapper
from pydantic import BaseModel


def spec_function(target_cls: Type[BaseModel]) -> Iterable[str]:
    return (field_name for field_name in target_cls.model_fields)


def extend(mapper: Mapper) -> None:
    mapper.add_spec(BaseModel, spec_function)
