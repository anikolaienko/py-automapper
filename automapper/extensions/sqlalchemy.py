from typing import Iterable, Type

from automapper import Mapper
from sqlalchemy.inspection import inspect
from sqlalchemy.orm import DeclarativeBase


def sqlalchemy_spec_decide(obj_type: Type[object]) -> bool:
    return inspect(obj_type, raiseerr=False) is not None


def spec_function(target_cls: Type[DeclarativeBase]) -> Iterable[str]:
    inspector = inspect(target_cls)
    attrs = [x.key for x in inspector.attrs]
    return attrs


def extend(mapper: Mapper) -> None:
    mapper.add_spec(sqlalchemy_spec_decide, spec_function)
