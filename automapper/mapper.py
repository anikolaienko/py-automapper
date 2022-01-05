from typing import (
    Any,
    Union,
    Type,
    TypeVar,
    Dict,
    Set,
    Callable,
    Iterable,
    Generic,
    overload,
    cast,
)
from copy import deepcopy
import inspect

from .exceptions import (
    CircularReferenceError,
    DuplicatedRegistrationError,
    MappingError,
)

# Custom Types
S = TypeVar("S")
T = TypeVar("T")
ClassifierFunction = Callable[[Type[T]], bool]
SpecFunction = Callable[[Type[T]], Iterable[str]]

__PRIMITIVE_TYPES = {int, float, complex, str, bytes, bytearray, bool}


def is_sequence(obj: Any) -> bool:
    """Check if object implements `__iter__` method"""
    return hasattr(obj, "__iter__")


def is_subscriptable(obj: Any) -> bool:
    """Check if object implements `__get_item__` method"""
    return hasattr(obj, "__get_item__")


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
    def add_spec(self, classifier: Type[T], spec_func: SpecFunction[T]) -> None:
        """Add a spec function for all classes in inherited from base class.

        Parameters:
            * classifier - base class to identify all descendant classes
            * spec_func - returns a list of fields (List[str]) for target class
            that are accepted in constructor
        """
        ...

    @overload
    def add_spec(
        self, classifier: ClassifierFunction[T], spec_func: SpecFunction[T]
    ) -> None:
        """Add a spec function for all classes identified by classifier function.

        Parameters:
            * classifier - boolean predicate that identifies a group of classes
            by certain characteristics: if class has a specific method or a field, etc.
            * spec_func - returns a list of fields (List[str]) for target class
            that are accepted in constructor
        """
        ...

    def add_spec(
        self,
        classifier: Union[Type[T], ClassifierFunction[T]],
        spec_func: SpecFunction[T],
    ) -> None:
        if inspect.isclass(classifier):
            if classifier in self._class_specs:
                raise DuplicatedRegistrationError(
                    f"Spec function for base class: {classifier} was already added"
                )
            self._class_specs[cast(Type[T], classifier)] = spec_func
        elif callable(classifier):
            if classifier in self._classifier_specs:
                raise DuplicatedRegistrationError(
                    f"Spec function for classifier {classifier} was already added"
                )
            self._classifier_specs[cast(ClassifierFunction[T], classifier)] = spec_func
        else:
            raise ValueError("Incorrect type of the classifier argument")

    def add(
        self, source_cls: Type[S], target_cls: Type[T], override: bool = False
    ) -> None:
        """Adds mapping between object of `source class` to an object of `target class`.

        Parameters
        ----------
        source_cls : Type
            Source class to map from
        target_cls : Type
            Target class to map to
        override : bool, optional
            Override existing `source class` mapping to use new `target class`
        """
        if source_cls in self._mappings and not override:
            raise DuplicatedRegistrationError(
                f"source_cls {source_cls} was already added for mapping"
            )
        self._mappings[source_cls] = target_cls

    def map(self, obj: object, skip_none_values: bool = False, **kwargs: Any) -> T:
        """Produces output object mapped from source object and custom arguments"""
        obj_type = type(obj)
        if obj_type not in self._mappings:
            raise MappingError(f"Missing mapping type for input type {obj_type}")

        return self._map_common(
            obj,
            self._mappings[obj_type],
            set(),
            skip_none_values=skip_none_values,
            **kwargs,
        )

    def _get_fields(self, target_cls: Type[T]) -> Iterable[str]:
        """Retrieved list of fields for initializing target class object"""
        for base_class in self._class_specs:
            if issubclass(target_cls, base_class):
                return self._class_specs[base_class](target_cls)

        for classifier in reversed(self._classifier_specs):
            if classifier(target_cls):
                return self._classifier_specs[classifier](target_cls)

        raise MappingError(
            f"No spec function is added for base class of {type(target_cls)}"
        )

    def _map_subobject(
        self, obj: S, _visited_stack: Set[int], skip_none_values: bool = False
    ) -> Any:
        """Maps subobjects recursively"""
        if is_primitive(obj):
            return obj

        obj_id = id(obj)
        if obj_id in _visited_stack:
            raise CircularReferenceError()

        if type(obj) in self._mappings:
            result = self._map_common(
                obj,
                self._mappings[type(obj)],
                _visited_stack,
                skip_none_values=skip_none_values,
            )
        else:
            _visited_stack.add(obj_id)

            if is_sequence(obj):
                if isinstance(obj, dict):
                    result = {
                        k: self._map_subobject(
                            v, _visited_stack, skip_none_values=skip_none_values
                        )
                        for k, v in obj
                    }
                else:
                    result = type(obj)(  # type: ignore [call-arg]
                        [
                            self._map_subobject(
                                x, _visited_stack, skip_none_values=skip_none_values
                            )
                            for x in cast(Iterable[Any], obj)
                        ]
                    )
            else:
                result = deepcopy(obj)

            _visited_stack.remove(obj_id)

        return result

    def _map_common(
        self,
        obj: S,
        target_cls: Type[T],
        _visited_stack: Set[int],
        skip_none_values: bool = False,
        **kwargs: Any,
    ) -> T:
        """Produces output object mapped from source object and custom arguments

        Parameters:
            skip_none_values - do not map fields that has None value
            **kwargs - custom mappings and fields overrides
        """
        obj_id = id(obj)

        if obj_id in _visited_stack:
            raise CircularReferenceError()
        _visited_stack.add(obj_id)

        target_cls_fields = self._get_fields(target_cls)

        mapped_values: Dict[str, Any] = {}
        is_obj_subscriptable = is_subscriptable(obj)
        for field_name in target_cls_fields:
            if (
                field_name in kwargs
                or hasattr(obj, field_name)
                or (is_obj_subscriptable and field_name in obj)  # type: ignore [operator]
            ):
                if field_name in kwargs:
                    value = kwargs[field_name]
                elif hasattr(obj, field_name):
                    value = getattr(obj, field_name)
                else:
                    value = obj[field_name]  # type: ignore [index]

                if value is not None:
                    mapped_values[field_name] = self._map_subobject(
                        value, _visited_stack, skip_none_values
                    )
                elif not skip_none_values:
                    mapped_values[field_name] = None

        _visited_stack.remove(obj_id)

        return target_cls(**mapped_values)  # type: ignore [call-arg]

    def to(self, target_cls: Type[T]) -> MappingWrapper[T]:
        """Specify target class to map source object to"""
        return MappingWrapper[T](self, target_cls)
