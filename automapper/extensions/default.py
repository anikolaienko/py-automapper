from typing import Type, TypeVar, Iterable

from automapper import Mapper

T = TypeVar("T")


# Predefined field extractors
# For any class with `__init__(self, ...)` constructor
def __init_method_verifier__(target_cls: Type[T]) -> bool:
    """Default field verifier for classes with described fields in `__init__` method.
    """
    return (
        hasattr(target_cls, "__init__")
        and hasattr(getattr(target_cls, "__init__"), "__annotations__")
        and isinstance(getattr(getattr(target_cls, "__init__"), "__annotations__"), dict)
    )


def __init_method_fields_extractor__(target_cls: Type[T]) -> Iterable[str]:
    """Default field extractor for classes with described fields in `__init__` method.
    If __init__ of the target class accepts `*args` or `**kwargs`
    then current extractor is no good and another verifier/extractor should be registered.
    """
    # TODO: check for fields like: ...arrays, *args, **kwargs
    return (field for field in target_cls.__init__.__annotations__.keys() if field != "return")


def extend(mapper: Mapper) -> None:
    mapper.register_fn_extractor(__init_method_verifier__, __init_method_fields_extractor__)
