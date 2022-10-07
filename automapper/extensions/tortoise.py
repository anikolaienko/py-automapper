from typing import Iterable, Type

from automapper import Mapper
from tortoise import Model


def spec_function(target_cls: Type[Model]) -> Iterable[str]:
    return (field_name for field_name in target_cls._meta.fields_map)


def extend(mapper: Mapper) -> None:
    mapper.add_spec(Model, spec_function)
