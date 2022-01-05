class DuplicatedRegistrationError(ValueError):
    pass


class MappingError(Exception):
    pass


class CircularReferenceError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(
            "Mapper does not support objects with circular references yet", *args
        )
