import inspect
from copy import deepcopy
from typing import (
    Any,
    Callable,
    Dict,
    Generic,
    Iterable,
    Optional,
    Set,
    Tuple,
    Type,
    TypeVar,
    Union,
    cast,
    overload,
)

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
FieldsMap = Optional[Dict[str, Any]]

__PRIMITIVE_TYPES = {int, float, complex, str, bytes, bytearray, bool}


def _is_sequence(obj: Any) -> bool:
    """Check if object implements `__iter__` method"""
    return hasattr(obj, "__iter__")


def _is_subscriptable(obj: Any) -> bool:
    """Check if object implements `__get_item__` method"""
    return hasattr(obj, "__get_item__")


def _is_primitive(obj: Any) -> bool:
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

    def map(
        self,
        obj: S,
        *,
        skip_none_values: bool = False,
        fields_mapping: FieldsMap = None,
        deepcopy: bool = True,
    ) -> T:
        """Produces output object mapped from source object and custom arguments.

        Parameters:
            skip_none_values - do not map fields that has None value
            fields_mapping - mapping for fields with different names
            deepcopy - should we deepcopy all attributes? [default: True]

        Args:
            obj (S): _description_
            skip_none_values (bool, optional): Skip None values when creating `target class` obj. Defaults to False.
            fields_mapping (FieldsMap, optional): Custom mapping.
                Specify dictionary in format {"field_name": value_object}. Defaults to None.
            deepcopy (bool, optional): Applies deepcopy to all child objects when copy into output instance.
                Defaults to True.

        Raises:
            CircularReferenceError: Circular references in `source class` object are not allowed yet.

        Returns:
            T: instance of `target class` with mapped values from `source class` or custom `fields_mapping` dictionary.
        """
        return self.__mapper._map_common(
            obj,
            self.__target_cls,
            set(),
            skip_none_values=skip_none_values,
            fields_mapping=fields_mapping,
            deepcopy=deepcopy,
        )


class Mapper:
    def __init__(self) -> None:
        """Initializes internal containers"""
        self._mappings: Dict[Type[S], Tuple[T, FieldsMap, bool]] = {}  # type: ignore [valid-type]
        self._class_specs: Dict[Type[T], SpecFunction[T]] = {}  # type: ignore [valid-type]
        self._classifier_specs: Dict[  # type: ignore [valid-type]
            ClassifierFunction[T], SpecFunction[T]
        ] = {}

    @overload
    def add_spec(self, classifier: Type[T], spec_func: SpecFunction[T]) -> None:
        """Add a spec function for all classes in inherited from base class.

        Args:
            classifier (ClassifierFunction[T]): base class to identify all descendant classes.
            spec_func (SpecFunction[T]): get list of fields (List[str]) for `target class` to be passed in constructor.
        """
        ...

    @overload
    def add_spec(
        self, classifier: ClassifierFunction[T], spec_func: SpecFunction[T]
    ) -> None:
        """Add a spec function for all classes identified by classifier function.

        Args:
            classifier (ClassifierFunction[T]): boolean predicate that identifies a group of classes
                by certain characteristics: if class has a specific method or a field, etc.
            spec_func (SpecFunction[T]): get list of fields (List[str]) for `target class` to be passed in constructor.
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
        self,
        source_cls: Type[S],
        target_cls: Type[T],
        override: bool = False,
        fields_mapping: FieldsMap = None,
        deepcopy: bool = True,
    ) -> None:
        """Adds mapping between object of `source class` to an object of `target class`.

        Args:
            source_cls (Type[S]): Source class to map from
            target_cls (Type[T]): Target class to map to
            override (bool, optional): Override existing `source class` mapping to use new `target class`.
                Defaults to False.
            fields_mapping (FieldsMap, optional): Custom mapping.
                Specify dictionary in format {"field_name": value_object}. Defaults to None.
            deepcopy (bool, optional): Applies deepcopy to all child objects when copy into output instance.
                Defaults to True.

        Raises:
            DuplicatedRegistrationError: Same mapping for `source class` was added.
            Only one mapping per source class can exist at a time for now.
            You can specify target class manually using `mapper.to(target_cls)` method
            or use `override` argument to replace existing mapping.
        """
        if source_cls in self._mappings and not override:
            raise DuplicatedRegistrationError(
                f"source_cls {source_cls} was already added for mapping"
            )
        self._mappings[source_cls] = (target_cls, fields_mapping, deepcopy)

    def map(
        self,
        obj: object,
        *,
        skip_none_values: bool = False,
        fields_mapping: FieldsMap = None,
        deepcopy: bool = True,
    ) -> T:  # type: ignore [type-var]
        """Produces output object mapped from source object and custom arguments

        Args:
            obj (object): Source object to map to `target class`.
            skip_none_values (bool, optional): Skip None values when creating `target class` obj. Defaults to False.
            fields_mapping (FieldsMap, optional): Custom mapping.
                Specify dictionary in format {"field_name": value_object}. Defaults to None.
            deepcopy (bool, optional): Applies deepcopy to all child objects when copy into output instance.
                Defaults to True.

        Raises:
            MappingError: No `target class` specified to be mapped into.
                Register mappings using `mapped.add(...)` or specify `target class` using `mapper.to(target_cls).map()`.
            CircularReferenceError: Circular references in `source class` object are not allowed yet.

        Returns:
            T: instance of `target class` with mapped values from `source class` or custom `fields_mapping` dictionary.
        """
        obj_type = type(obj)
        if obj_type not in self._mappings:
            raise MappingError(f"Missing mapping type for input type {obj_type}")
        obj_type_preffix = f"{obj_type.__name__}."

        target_cls, target_cls_field_mappings, target_deepcopy = self._mappings[
            obj_type
        ]

        common_fields_mapping = fields_mapping
        if target_cls_field_mappings:
            # transform mapping if it's from source class field
            common_fields_mapping = {
                target_obj_field: getattr(obj, source_field[len(obj_type_preffix) :])
                if isinstance(source_field, str)
                and source_field.startswith(obj_type_preffix)
                else source_field
                for target_obj_field, source_field in target_cls_field_mappings.items()
            }
            if fields_mapping:
                common_fields_mapping = {
                    **common_fields_mapping,
                    **fields_mapping,
                }  # merge two dict into one, fields_mapping has priority

        # If deepcopy is not explicitly given, we use target_deepcopy
        if deepcopy is None:
            deepcopy = target_deepcopy

        return self._map_common(
            obj,
            target_cls,
            set(),
            skip_none_values=skip_none_values,
            fields_mapping=common_fields_mapping,
            deepcopy=deepcopy,
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
        if _is_primitive(obj):
            return obj

        obj_id = id(obj)
        if obj_id in _visited_stack:
            raise CircularReferenceError()

        if type(obj) in self._mappings:
            target_cls, _, _ = self._mappings[type(obj)]
            result: Any = self._map_common(
                obj, target_cls, _visited_stack, skip_none_values=skip_none_values
            )
        else:
            _visited_stack.add(obj_id)

            if _is_sequence(obj):
                if isinstance(obj, dict):
                    result = {
                        k: self._map_subobject(
                            v, _visited_stack, skip_none_values=skip_none_values
                        )
                        for k, v in obj.items()
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
        fields_mapping: FieldsMap = None,
        deepcopy: bool = True,
    ) -> T:
        """Produces output object mapped from source object and custom arguments.

        Args:
            obj (S): Source object to map to `target class`.
            target_cls (Type[T]): Target class to map to.
            _visited_stack (Set[int]): Visited child objects. To avoid infinite recursive calls.
            skip_none_values (bool, optional): Skip None values when creating `target class` obj. Defaults to False.
            fields_mapping (FieldsMap, optional): Custom mapping.
                Specify dictionary in format {"field_name": value_object}. Defaults to None.
            deepcopy (bool, optional): Applies deepcopy to all child objects when copy into output instance.
                Defaults to True.

        Raises:
            CircularReferenceError: Circular references in `source class` object are not allowed yet.

        Returns:
            T: Instance of `target class` with mapped fields.
        """
        obj_id = id(obj)

        if obj_id in _visited_stack:
            raise CircularReferenceError()
        _visited_stack.add(obj_id)

        target_cls_fields = self._get_fields(target_cls)

        mapped_values: Dict[str, Any] = {}
        is_obj_subscriptable = _is_subscriptable(obj)
        for field_name in target_cls_fields:
            if (
                (fields_mapping and field_name in fields_mapping)
                or hasattr(obj, field_name)
                or (is_obj_subscriptable and field_name in obj)  # type: ignore [operator]
            ):
                if fields_mapping and field_name in fields_mapping:
                    value = fields_mapping[field_name]
                elif hasattr(obj, field_name):
                    value = getattr(obj, field_name)
                else:
                    value = obj[field_name]  # type: ignore [index]

                if value is not None:
                    if deepcopy:
                        mapped_values[field_name] = self._map_subobject(
                            value, _visited_stack, skip_none_values
                        )
                    else:
                        # if deepcopy is disabled, we can act as if value was a primitive type and
                        # avoid the ._map_subobject() call entirely.
                        mapped_values[field_name] = value
                elif not skip_none_values:
                    mapped_values[field_name] = None

        _visited_stack.remove(obj_id)

        return cast(target_cls, target_cls(**mapped_values))  # type: ignore [valid-type]

    def to(self, target_cls: Type[T]) -> MappingWrapper[T]:
        """Specify `target class` to which map `source class` object.

        Args:
            target_cls (Type[T]): Target class.

        Returns:
            MappingWrapper[T]: Mapping wrapper. Use `map` method to perform mapping now.
        """
        return MappingWrapper[T](self, target_cls)
