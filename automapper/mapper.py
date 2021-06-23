from typing import Type, TypeVar, Dict, List, Tuple, Callable, Iterable, Optional
import dataclasses

from .exceptions import DuplicatedRegistration, MappingError

## Custom Types
BaseType = TypeVar("BaseType", Type, object)
FieldExtractor = Callable[[Type], Iterable[str]]
ExtractorVerifier = Callable[[Type], bool]

## Internal containers
__MAPPINGS__: Dict[Type, Type] = {}
__FIELD_EXTRACTORS__: Dict[Type, FieldExtractor] = {}
__FIELD_EXTRACTORS_WITH_VERIFIER__: Dict[ExtractorVerifier, FieldExtractor] = {}


def register_cls_extractor(base_class: Type, field_extractor: FieldExtractor) -> None:
    if base_class in __FIELD_EXTRACTORS__:
        raise DuplicatedRegistration(f"Field extractor for base class: {base_class} is already registered")
    __FIELD_EXTRACTORS__[base_class] = field_extractor


def register_fn_extractor(verifier: ExtractorVerifier, field_extractor: FieldExtractor) -> None:
    if verifier in __FIELD_EXTRACTORS_WITH_VERIFIER__:
        raise DuplicatedRegistration(f"Field extractor for verifier {verifier} is already registered")
    __FIELD_EXTRACTORS_WITH_VERIFIER__[verifier] = field_extractor


# Predefined field extractors and class verifiers
## For dataclass
def __dataclass_verifier__(target_cls: Type) -> bool:
    return dataclasses.is_dataclass(target_cls)


def __dataclass_field_extractor__(target_cls: Type) -> Iterable[str]:
    return (x.name for x in dataclasses.fields(target_cls))

## For any class with `__init__(self, ...)` constructor
def __init_method_verifier__(target_cls) -> bool:
    return hasattr(target_cls, "__init__")                  \
        and hasattr(target_cls.__init__, "__annotations__") \
        and isinstance(target_cls.__init__.__annotations__, dict)


def __init_method_fields_extractor__(target_cls: Type) -> Iterable[str]:
    return (field for field in target_cls.__init__.__annotations__.keys() if field != 'return')

## Registering default extractors
register_fn_extractor(__dataclass_verifier__, __dataclass_field_extractor__)
register_fn_extractor(__init_method_verifier__, __init_method_fields_extractor__)


def add(source_cls: Type, target_cls: Type):  # TODO: add custom mappings for fields
    if source_cls in __MAPPINGS__:
        raise DuplicatedRegistration(f"source_cls {source_cls} is already registered for mapping")
    __MAPPINGS__[source_cls] = target_cls


def __get_fields__(target_cls: Type) -> Iterable[str]:
    for verifier in __FIELD_EXTRACTORS_WITH_VERIFIER__:
        if verifier(target_cls):
            return __FIELD_EXTRACTORS_WITH_VERIFIER__[verifier](target_cls)
    for base_class in __FIELD_EXTRACTORS__:
        if issubclass(target_cls, base_class):
            return __FIELD_EXTRACTORS__[base_class](target_cls)
    raise MappingError(f"No fields extractor registered for base class of {type(target_cls)}")


def map(obj: object) -> object:
    obj_type = type(obj)
    if obj_type not in __MAPPINGS__:
        raise MappingError(f"Missing mapping type for input type {obj_type}")
    
    mapping_type = __MAPPINGS__[obj_type]
    to_fields = __get_fields__(mapping_type)

    mapped_values = {}
    for field_name in to_fields:
        if hasattr(obj, field_name):
            mapped_values[field_name] = getattr(obj, field_name)
    
    return mapping_type(**mapped_values)


def to(target_cls: Type):
    raise NotImplementedError()
