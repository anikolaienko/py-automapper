from typing import Any, Type, TypeVar, Dict, Callable, Iterable, Generic
from copy import deepcopy

from .exceptions import CircularReferenceError, DuplicatedRegistrationError, MappingError

# Custom Types
S = TypeVar("S")
T = TypeVar("T")
FieldExtractor = Callable[[Type[T]], Iterable[str]]
ExtractorVerifier = Callable[[Type[T]], bool]

__PRIMITIVE_TYPES = {int, float, complex, str, bytes, bytearray, bool}


def __is_sequence(obj: Any) -> bool:
    """Check if object is iteratable"""
    return hasattr(obj, '__iter__') 


def __is_primitive(obj: Any) -> bool:
    """Check if object type is primitive"""
    return type(obj) in __PRIMITIVE_TYPES


class __MappingWrapper__(Generic[T]):
    """Internal wrapper for supporting syntax:
    ```
    mapper.to(TargetClass).map(SourceObject)
    ```
    """

    def __init__(self, mapper: "Mapper", target_cls: Type[T]) -> None:
        """Stores mapper and target class for using into `map` method"""
        self.__target_cls = target_cls
        self.__mapper = mapper

    def map(self, obj: S, skip_none_values: bool = False, **kwargs: Any) -> T:
        """Produces output object mapped from source object and custom arguments
        
        Parameters:
            skip_none_values - do not map fields that has None value
            **kwargs - custom mappings and fields overrides
        """
        return self.__mapper.__map_common(
            obj, self.__target_cls, set(), skip_none_values=skip_none_values
        )


class Mapper:
    def __init__(self) -> None:
        """Initializes internal containers"""
        self.__MAPPINGS__: Dict[Type[S], Type[T]] = {}  # type: ignore [valid-type]
        self.__FIELD_EXTRACTORS__: Dict[  # type: ignore [valid-type]
            Type[T], FieldExtractor[T]
        ] = {}
        self.__FIELD_EXTRACTORS_WITH_VERIFIER__: Dict[  # type: ignore [valid-type]
            ExtractorVerifier[T], FieldExtractor[T]
        ] = {}

    def register_cls_extractor(self, base_cls: Type[T], field_extractor: FieldExtractor[T]) -> None:
        """Register a function that produces list of fields for a class inherited from base class"""
        if base_cls in self.__FIELD_EXTRACTORS__:
            raise DuplicatedRegistrationError(
                f"Field extractor for base class: {base_cls} is already registered"
            )
        self.__FIELD_EXTRACTORS__[base_cls] = field_extractor

    def register_fn_extractor(
        self, verifier: ExtractorVerifier[T], field_extractor: FieldExtractor[T]
    ) -> None:
        """Register two functions:
            verifier - a function that can identify specific type of objects
            field_extractor - a function that can produces list of fields for identified type of object
        """
        if verifier in self.__FIELD_EXTRACTORS_WITH_VERIFIER__:
            raise DuplicatedRegistrationError(
                f"Field extractor for verifier {verifier} is already registered"
            )
        self.__FIELD_EXTRACTORS_WITH_VERIFIER__[verifier] = field_extractor

    def add(
        self, source_cls: Type[S], target_cls: Type[T]
    ) -> None:
        """Adds mapping between object of source class to form an object of target class"""
        if source_cls in self.__MAPPINGS__:
            raise DuplicatedRegistrationError(
                f"source_cls {source_cls} is already registered for mapping"
            )
        self.__MAPPINGS__[source_cls] = target_cls

    def map(self, obj: object, skip_none_values: bool = False) -> object:
        """Produces output object mapped from source object and custom arguments"""
        obj_type = type(obj)
        if obj_type not in self.__MAPPINGS__:
            raise MappingError(f"Missing mapping type for input type {obj_type}")

        return self.__map_common(
            obj, self.__MAPPINGS__[obj_type], set(), skip_none_values=skip_none_values
        )

    def __get_fields(self, target_cls: Type[T]) -> Iterable[str]:
        """Retrieved list of fields for initializing target class object"""
        for base_class in self.__FIELD_EXTRACTORS__:
            if issubclass(target_cls, base_class):
                return self.__FIELD_EXTRACTORS__[base_class](target_cls)

        for verifier in self.__FIELD_EXTRACTORS_WITH_VERIFIER__:
            if verifier(target_cls):
                return self.__FIELD_EXTRACTORS_WITH_VERIFIER__[verifier](target_cls)

        raise MappingError(f"No fields extractor registered for base class of {type(target_cls)}")

    def __map_subobject(self, obj: S, _visited_objects: set, skip_none_values: bool = False) -> T:
        """
        """
        if __is_primitive(obj):
            return obj

        if id(obj) in _visited_objects:
            raise CircularReferenceError("Mapper does not support objects with circular references")
        _visited_objects.add(id(obj))

        if __is_sequence(obj):
            if isinstance(obj, dict):
                return {
                    k: self.__map_subobject(v, skip_none_values=skip_none_values)
                    for k, v in obj
                }
            else:
                return type(obj)([
                    self.__map_subobject(x, skip_none_values=skip_none_values)
                    for x in obj
                ])

        if type(obj) in self.__MAPPINGS__:
            return self.__map_common(
                obj,
                self.__MAPPINGS__[type(obj)],
                skip_none_values=skip_none_values
            )

        return deepcopy(obj)


    def __map_common(self, obj: S, target_cls: Type[T], _visited_objects: set, skip_none_values: bool = False, **kwargs: Any) -> T:
        """Produces output object mapped from source object and custom arguments
        
        Parameters:
            skip_none_values - do not map fields that has None value
            **kwargs - custom mappings and fields overrides
        """
        if id(obj) in _visited_objects:
            raise CircularReferenceError("Mapper does not support objects with circular references")
        _visited_objects.add(id(obj))

        target_cls_fields = self.__get_fields(target_cls)

        mapped_values = {}
        for field_name in target_cls_fields:
            if field_name in kwargs or hasattr(obj, field_name):
                value = kwargs[field_name] if field_name in kwargs else getattr(obj, field_name)

                if value is not None:
                    mapped_values[field_name] = self.__map_subobject(value, _visited_objects, skip_none_values)
                elif not skip_none_values:
                    mapped_values[field_name] = None

        return target_cls(**mapped_values)  # type: ignore [call-arg]

    def to(self, target_cls: Type[T]) -> __MappingWrapper__[T]:
        """Specify target class to map source object to"""
        return __MappingWrapper__[T](self, target_cls)


# Global mapper
mapper = Mapper()
