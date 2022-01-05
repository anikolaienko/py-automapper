# flake8: noqa: F401
from .mapper import Mapper

from .exceptions import (
    DuplicatedRegistrationError,
    MappingError,
    CircularReferenceError,
)

from .mapper_initializer import create_mapper

# Global mapper
mapper = create_mapper()
