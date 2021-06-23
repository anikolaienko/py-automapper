from typing import Type, TypeVar, Dict, List, Tuple, Callable, Iterable
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


def register_extractor(base_class: Type, field_extractor: FieldExtractor) -> None:
    if base_class in __FIELD_EXTRACTORS__:
        raise DuplicatedRegistration(f"Field extractor for base class: {base_class} is already registered")
    __FIELD_EXTRACTORS__[base_class] = field_extractor

# TODO: add extension
# def register_extractor(verifier: ExtractorVerifier, field_extractor: FieldExtractor) -> None:
#     if verifier in __FIELD_EXTRACTORS_WITH_VERIFIER__:
#         raise DuplicatedRegistration(f"Field extractor for verifier {verifier} is already registered")
#     __FIELD_EXTRACTORS_WITH_VERIFIER__[verifier] = field_extractor


def __dataclass_verifier__(concrete_class: Type) -> bool:
    return dataclasses.is_dataclass(concrete_class)


def __dataclass_field_extractor__(concrete_class: Type) -> Iterable[str]:
    return (x.name for x in dataclasses.fields(concrete_class))


register_extractor(__dataclass_verifier__, __dataclass_field_extractor__)


def add(from_class: Type, to_class: Type):  # TODO: add custom mappings for fields
    if from_class in __MAPPINGS__:
        raise DuplicatedRegistration(f"from_class {from_class} is already registered for mapping")
    __MAPPINGS__[from_class] = to_class


def __get_fields__(obj, object) -> Iterable[str]:
    for verifier in __FIELD_EXTRACTORS_WITH_VERIFIER__:
        if verifier(obj):
            return __FIELD_EXTRACTORS_WITH_VERIFIER__[verifier](obj)
    for base_class in __FIELD_EXTRACTORS__:
        if isinstance(obj, base_class):
            return __FIELD_EXTRACTORS__[base_class](obj)
    raise MappingError(f"No fields extractor registered for base class of {type(obj)}")


def map(obj: object) -> object:
    obj_type = type(obj)
    if obj_type not in __MAPPINGS__:
        raise MappingError(f"Missing mapping type for input type {obj_type}")
    
    mapping_type = __MAPPINGS__[obj_type]
    to_fields = __get_fields__(obj)

    mapped_values = {}
    for field_name in to_fields:
        if hasattr(obj, field_name):
            mapped_values[field_name] = getattr(obj, field_name)
    
    return mapping_type(**mapped_values)


# def to()

