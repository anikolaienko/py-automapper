# flake8: noqa: F401
from .exceptions import (
    CircularReferenceError,
    DuplicatedRegistrationError,
    MappingError,
)
from .mapper import Mapper
from .mapper_initializer import create_mapper

# Global mapper
mapper = create_mapper()
