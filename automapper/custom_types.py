from typing import Any, Callable, Dict, Iterable, Optional, Type, TypeVar

from automapper.path_mapper import MapPath

# Custom Types
S = TypeVar("S")
T = TypeVar("T")
ClassifierFunction = Callable[[Type[T]], bool]
SpecFunction = Callable[[Type[T]], Iterable[str]]
FieldsMap = Optional[Dict[str | MapPath, Any]]
