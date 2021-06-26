from typing import Type, Iterable

from tortoise import Model

from automapper import Mapper


def fields_extractor(target_cls: Type[Model]) -> Iterable[str]:
    return (field_name for field_name in target_cls._meta.fields_map)


def extend(mapper: Mapper) -> None:
    mapper.register_cls_extractor(Model, fields_extractor)
