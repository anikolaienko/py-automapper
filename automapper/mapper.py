from typing import Type, TypeVar, Dict, Callable, Iterable, Generic

from .exceptions import DuplicatedRegistration, MappingError

# Custom Types
S = TypeVar("S")
T = TypeVar("T")
FieldExtractor = Callable[[Type[T]], Iterable[str]]
ExtractorVerifier = Callable[[Type[T]], bool]

# Internal containers
__MAPPINGS__: Dict[Type[S], Type[T]] = {}  # type: ignore [valid-type]
__FIELD_EXTRACTORS__: Dict[Type[T], FieldExtractor[T]] = {}  # type: ignore [valid-type]
__FIELD_EXTRACTORS_WITH_VERIFIER__: Dict[  # type: ignore [valid-type]
    ExtractorVerifier[T], FieldExtractor[T]
] = {}


def register_cls_extractor(base_cls: Type[T], field_extractor: FieldExtractor[T]) -> None:
    """TODO: add description"""
    if base_cls in __FIELD_EXTRACTORS__:
        raise DuplicatedRegistration(
            f"Field extractor for base class: {base_cls} is already registered"
        )
    __FIELD_EXTRACTORS__[base_cls] = field_extractor


def register_fn_extractor(
    verifier: ExtractorVerifier[T], field_extractor: FieldExtractor[T]
) -> None:
    """TODO: add description"""
    if verifier in __FIELD_EXTRACTORS_WITH_VERIFIER__:
        raise DuplicatedRegistration(
            f"Field extractor for verifier {verifier} is already registered"
        )
    __FIELD_EXTRACTORS_WITH_VERIFIER__[verifier] = field_extractor


# Predefined field extractors and class verifiers
# For any class with `__init__(self, ...)` constructor
def __init_method_verifier__(target_cls: Type[T]) -> bool:
    """TODO: add description"""
    return (
        hasattr(target_cls, "__init__")
        and hasattr(getattr(target_cls, "__init__"), "__annotations__")
        and isinstance(getattr(getattr(target_cls, "__init__"), "__annotations__"), dict)
    )


def __init_method_fields_extractor__(target_cls: Type[T]) -> Iterable[str]:
    """TODO: add description"""
    return (field for field in target_cls.__init__.__annotations__.keys() if field != "return")


# Registering default extractors
register_fn_extractor(__init_method_verifier__, __init_method_fields_extractor__)


def add(source_cls: Type[S], target_cls: Type[T]) -> None:  # TODO: add custom mappings for fields
    """TODO: add description"""
    if source_cls in __MAPPINGS__:
        raise DuplicatedRegistration(f"source_cls {source_cls} is already registered for mapping")
    __MAPPINGS__[source_cls] = target_cls


def __get_fields__(target_cls: Type[T]) -> Iterable[str]:
    """TODO: add description"""
    for base_class in __FIELD_EXTRACTORS__:
        if issubclass(target_cls, base_class):
            return __FIELD_EXTRACTORS__[base_class](target_cls)

    for verifier in __FIELD_EXTRACTORS_WITH_VERIFIER__:
        if verifier(target_cls):
            return __FIELD_EXTRACTORS_WITH_VERIFIER__[verifier](target_cls)

    raise MappingError(f"No fields extractor registered for base class of {type(target_cls)}")


def __map_common__(obj: S, target_cls: Type[T], skip_none_values = False) -> T:
    """TODO: add description"""
    target_cls_fields = __get_fields__(target_cls)

    mapped_values = {}
    for field_name in target_cls_fields:
        if hasattr(obj, field_name):
            value = getattr(obj, field_name)

            if not skip_none_values or value is not None:
                mapped_values[field_name] = value

    return target_cls(**mapped_values)  # type: ignore [call-arg]


def map(obj: object, skip_none_values = False) -> object:
    """TODO: add description"""
    obj_type = type(obj)
    if obj_type not in __MAPPINGS__:
        raise MappingError(f"Missing mapping type for input type {obj_type}")

    return __map_common__(obj, __MAPPINGS__[obj_type], skip_none_values=skip_none_values)


class MappingWrapper(Generic[T]):
    """TODO: add description"""

    def __init__(self, target_cls: Type[T]) -> None:
        """TODO: add description"""
        self.__target_cls = target_cls

    def map(self, obj: S, skip_none_values = False) -> T:
        """TODO: add description"""
        return __map_common__(obj, self.__target_cls, skip_none_values=skip_none_values)


def to(target_cls: Type[T]) -> MappingWrapper[T]:
    """TODO: add description"""
    return MappingWrapper[T](target_cls)
