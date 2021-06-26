# flake8: noqa: F401
from .mapper import Mapper, mapper

from .exceptions import DuplicatedRegistrationError, MappingError

from .extensions_loader import load_extensions

load_extensions(mapper)
