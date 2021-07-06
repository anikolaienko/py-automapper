from typing import Any, Union, Type, TypeVar, Dict, Set, Callable, Iterable, Generic, overload
from copy import deepcopy
import inspect

from .exceptions import CircularReferenceError, DuplicatedRegistrationError, MappingError

# Custom Types
S = TypeVar("S")
T = TypeVar("T")
ClassifierFunction = Callable[[Type[T]], bool]
SpecFunction = Callable[[Type[T]], Iterable[str]]

__PRIMITIVE_TYPES = {int, float, complex, str, bytes, bytearray, bool}


def is_sequence(obj: Any) -> bool:
    """Check if object is iteratable"""
    return hasattr(obj, "__iter__")


def is_primitive(obj: Any) -> bool:
    """Check if object type is primitive"""
    return type(obj) in __PRIMITIVE_TYPES


class MappingWrapper(Generic[T]):
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
        return self.__mapper._map_common(
            obj, self.__target_cls, set(), skip_none_values=skip_none_values
        )


class Mapper:
    def __init__(self) -> None:
        """Initializes internal containers"""
        self._mappings: Dict[Type[S], Type[T]] = {}  # type: ignore [valid-type]
        self._class_specs: Dict[Type[T], SpecFunction[T]] = {}  # type: ignore [valid-type]
        self._classifier_specs: Dict[  # type: ignore [valid-type]
            ClassifierFunction[T], SpecFunction[T]
        ] = {}

    @overload
    def add_spec(self, base_cls: Type[T], spec_func: SpecFunction[T]) -> None:
        """Add a spec function for all classes in inherited from base class.

        Parameters:
            * base_cls - base class to identify all descendant classes
            * spec_func - returns a list of fields (List[str]) for target class
            that are accepted in constructor
        """
        ...

    @overload
    def add_spec(self, classifier: ClassifierFunction[T], spec_func: SpecFunction[T]) -> None:
        """Add a spec function for all classes identified by classifier function.

        Parameters:
            * classifier - boolean predicate that identifies a group of classes
            by certain characteristics: if class has a specific method or a field, etc.
            * spec_func - returns a list of fields (List[str]) for target class
            that are accepted in constructor
        """
        ...

    def add_spec(
        self, classifier: Union[Type[T], ClassifierFunction[T]], spec_func: SpecFunction[T]
    ) -> None:
        if inspect.isclass(classifier):
            if classifier in self._class_specs:
                raise DuplicatedRegistrationError(
                    f"Spec function for base class: {classifier} was already added"
                )
            self._class_specs[classifier] = spec_func
        elif callable(classifier):
            if classifier in self._classifier_specs:
                raise DuplicatedRegistrationError(
                    f"Spec function for classifier {classifier} was already added"
                )
            self._classifier_specs[classifier] = spec_func
        else:
            raise ValueError("Incorrect type of the classifier argument")

    def add(self, source_cls: Type[S], target_cls: Type[T]) -> None:
        """Adds mapping between object of source class to form an object of target class"""
        if source_cls in self._mappings:
            raise DuplicatedRegistrationError(
                f"source_cls {source_cls} was already added for mapping"
            )
        self._mappings[source_cls] = target_cls

    def map(self, obj: object, skip_none_values: bool = False) -> object:
        """Produces output object mapped from source object and custom arguments"""
        obj_type = type(obj)
        if obj_type not in self._mappings:
            raise MappingError(f"Missing mapping type for input type {obj_type}")

        return self._map_common(
            obj, self._mappings[obj_type], set(), skip_none_values=skip_none_values
        )

    def _get_fields(self, target_cls: Type[T]) -> Iterable[str]:
        """Retrieved list of fields for initializing target class object"""
        for base_class in self._class_specs:
            if issubclass(target_cls, base_class):
                return self._class_specs[base_class](target_cls)

        for classifier in self._classifier_specs:
            if classifier(target_cls):
                return self._classifier_specs[classifier](target_cls)

        raise MappingError(f"No spec function is added for base class of {type(target_cls)}")

    def _map_subobject(self, obj: S, _visited_objects: set, skip_none_values: bool = False) -> Any:
        """"""
        if is_primitive(obj):
            return obj

        if id(obj) in _visited_objects:
            raise CircularReferenceError("Mapper does not support objects with circular references")
        _visited_objects.add(id(obj))

        if is_sequence(obj):
            if isinstance(obj, dict):
                return {
                    k: self._map_subobject(v, skip_none_values=skip_none_values) for k, v in obj
                }
            else:
                return type(obj)(
                    [self._map_subobject(x, skip_none_values=skip_none_values) for x in obj]
                )

        if type(obj) in self._mappings:
            return self._map_common(
                obj, self._mappings[type(obj)], skip_none_values=skip_none_values
            )

        return deepcopy(obj)

    def _map_common(
        self,
        obj: S,
        target_cls: Type[T],
        _visited_objects: Set[int],
        skip_none_values: bool = False,
        **kwargs: Any,
    ) -> T:
        """Produces output object mapped from source object and custom arguments

        Parameters:
            skip_none_values - do not map fields that has None value
            **kwargs - custom mappings and fields overrides
        """
        if id(obj) in _visited_objects:
            raise CircularReferenceError("Mapper does not support objects with circular references")
        _visited_objects.add(id(obj))

        target_cls_fields = self._get_fields(target_cls)

        mapped_values: Dict[str, Any] = {}
        for field_name in target_cls_fields:
            if field_name in kwargs or hasattr(obj, field_name):
                value = kwargs[field_name] if field_name in kwargs else getattr(obj, field_name)

                if value is not None:
                    mapped_values[field_name] = self._map_subobject(
                        value, _visited_objects, skip_none_values
                    )
                elif not skip_none_values:
                    mapped_values[field_name] = None

        return target_cls(**mapped_values)  # type: ignore [call-arg]

    def to(self, target_cls: Type[T]) -> MappingWrapper[T]:
        """Specify target class to map source object to"""
        return MappingWrapper[T](self, target_cls)


# Global mapper
mapper = Mapper()
