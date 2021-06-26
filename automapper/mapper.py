from typing import Type, TypeVar, Dict, Callable, Iterable, Generic

from .exceptions import DuplicatedRegistrationError, MappingError

# Custom Types
S = TypeVar("S")
T = TypeVar("T")
FieldExtractor = Callable[[Type[T]], Iterable[str]]
ExtractorVerifier = Callable[[Type[T]], bool]


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

    def map(self, obj: S, skip_none_values: bool = False) -> T:
        """Produces output object mapped from source object and custom arguments"""
        return self.__mapper.__map_common__(
            obj, self.__target_cls, skip_none_values=skip_none_values
        )


class Mapper:
    def __init__(self) -> None:
        # Internal containers
        self.__MAPPINGS__: Dict[Type[S], Type[T]] = {}  # type: ignore [valid-type]
        self.__FIELD_EXTRACTORS__: Dict[  # type: ignore [valid-type]
            Type[T], FieldExtractor[T]
        ] = {}
        self.__FIELD_EXTRACTORS_WITH_VERIFIER__: Dict[  # type: ignore [valid-type]
            ExtractorVerifier[T], FieldExtractor[T]
        ] = {}

    def register_cls_extractor(self, base_cls: Type[T], field_extractor: FieldExtractor[T]) -> None:
        """TODO: add description"""
        if base_cls in self.__FIELD_EXTRACTORS__:
            raise DuplicatedRegistrationError(
                f"Field extractor for base class: {base_cls} is already registered"
            )
        self.__FIELD_EXTRACTORS__[base_cls] = field_extractor

    def register_fn_extractor(
        self, verifier: ExtractorVerifier[T], field_extractor: FieldExtractor[T]
    ) -> None:
        """TODO: add description"""
        if verifier in self.__FIELD_EXTRACTORS_WITH_VERIFIER__:
            raise DuplicatedRegistrationError(
                f"Field extractor for verifier {verifier} is already registered"
            )
        self.__FIELD_EXTRACTORS_WITH_VERIFIER__[verifier] = field_extractor

    def add(
        self, source_cls: Type[S], target_cls: Type[T]
    ) -> None:  # TODO: add custom mappings for fields
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

        return self.__map_common__(
            obj, self.__MAPPINGS__[obj_type], skip_none_values=skip_none_values
        )

    def __get_fields__(self, target_cls: Type[T]) -> Iterable[str]:
        """TODO: add description"""
        for base_class in self.__FIELD_EXTRACTORS__:
            if issubclass(target_cls, base_class):
                return self.__FIELD_EXTRACTORS__[base_class](target_cls)

        for verifier in self.__FIELD_EXTRACTORS_WITH_VERIFIER__:
            if verifier(target_cls):
                return self.__FIELD_EXTRACTORS_WITH_VERIFIER__[verifier](target_cls)

        raise MappingError(f"No fields extractor registered for base class of {type(target_cls)}")

    def __map_common__(self, obj: S, target_cls: Type[T], skip_none_values: bool = False) -> T:
        """TODO: add description"""
        target_cls_fields = self.__get_fields__(target_cls)

        mapped_values = {}
        for field_name in target_cls_fields:
            if hasattr(obj, field_name):
                value = getattr(obj, field_name)

                if not skip_none_values or value is not None:
                    mapped_values[field_name] = value

        return target_cls(**mapped_values)  # type: ignore [call-arg]

    def to(self, target_cls: Type[T]) -> __MappingWrapper__[T]:
        """TODO: add description"""
        return __MappingWrapper__[T](self, target_cls)


# Global mapper
mapper = Mapper()
