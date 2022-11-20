from enum import Enum, IntEnum

from automapper import mapper


class StringEnum(str, Enum):
    Value1 = "value1"
    Value2 = "value2"
    Value3 = "value3"


class IntValueEnum(IntEnum):
    Value1 = 1
    Value2 = 2
    Value3 = 3


class TupleEnum(Enum):
    Value1 = ("value", "1")
    Value2 = ("value", "2")
    Value3 = ("value", "3")


class SourceClass:
    def __init__(
        self, string_value: StringEnum, int_value: IntValueEnum, tuple_value: TupleEnum
    ) -> None:
        self.string_value = string_value
        self.int_value = int_value
        self.tuple_value = tuple_value


class TargetClass:
    def __init__(
        self, string_value: StringEnum, int_value: IntValueEnum, tuple_value: TupleEnum
    ) -> None:
        self.string_value = string_value
        self.int_value = int_value
        self.tuple_value = tuple_value


def test_map__enum():
    src = SourceClass(StringEnum.Value1, IntValueEnum.Value2, TupleEnum.Value3)
    dst = mapper.to(TargetClass).map(src)

    assert dst.string_value == StringEnum.Value1
    assert dst.int_value == IntValueEnum.Value2
    assert dst.tuple_value == TupleEnum.Value3
