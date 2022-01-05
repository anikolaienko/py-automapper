from typing import Type, TypeVar, Iterable

from automapper import Mapper


T = TypeVar("T")
_IGNORED_FIELDS = ("return", "args", "kwargs")


def __init_method_classifier__(target_cls: Type[T]) -> bool:
    """Default classifier for classes with described fields in `__init__` method"""
    return (
        hasattr(target_cls, "__init__")
        and hasattr(getattr(target_cls, "__init__"), "__annotations__")
        and isinstance(
            getattr(getattr(target_cls, "__init__"), "__annotations__"), dict
        )
    )


def __init_method_spec_func__(target_cls: Type[T]) -> Iterable[str]:
    """Default spec function for classes with described fields in `__init__` method.
    If __init__ of the target class accepts `*args` or `**kwargs`
    then current spec function won't work properly and another spec_func should be added
    """
    return (
        field
        for field in target_cls.__init__.__annotations__.keys()
        if field not in _IGNORED_FIELDS
    )


def extend(mapper: Mapper) -> None:
    mapper.add_spec(__init_method_classifier__, __init_method_spec_func__)
