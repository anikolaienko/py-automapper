from sqlalchemy import inspect

from typing import Type, Iterable

from automapper import Mapper


def sqlalchemy_spec_decide(obj_type: Type[object]) -> bool:
    return inspect(obj_type, raiseerr=False) is not None


def spec_function(target_cls: Type[object]) -> Iterable[str]:
    inspector = inspect(target_cls)
    attrs = [x.key for x in inspector.attrs]
    return attrs


def extend(mapper: Mapper) -> None:
    mapper.add_spec(sqlalchemy_spec_decide, spec_function)
