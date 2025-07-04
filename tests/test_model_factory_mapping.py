from decimal import Decimal
from enum import Enum
from typing import Union
from unittest import TestCase

import pytest

from automapper import create_mapper


class SourceEnum(Enum):
    VALUE1 = "value1"
    VALUE2 = "value2"
    VALUE3 = "value3"

class NameEnum(Enum):
    VALUE1 = 1
    VALUE2 = 2
    VALUE3 = 3

class ValueEnum(Enum):
    A = "value1"
    B = "value2"
    C = "value3"

class ValueObject:
    value: str

    def __init__(self, value: Union[float, int, Decimal]):
        self.value = str(value)

    def __repr__(self):
        return f"ValueObject(value={self.value})"

    def __str__(self):
        return f"ValueObject(value={self.value})"

class AutomapperModelFactoryTest(TestCase):
    def setUp(self) -> None:
        self.mapper = create_mapper()

    def test_map__with_registered_lambda_factory(self):
        self.mapper.add(SourceEnum, NameEnum, model_factory=lambda x: NameEnum[x.name])
        self.mapper.add(ValueEnum, SourceEnum, model_factory=lambda x: SourceEnum(x.value))

        self.assertEqual(self.mapper.map(SourceEnum.VALUE3), NameEnum.VALUE3)
        self.assertEqual(self.mapper.map(ValueEnum.B), SourceEnum.VALUE2)


    def test_map__with_lambda_factory(self):
        name_enum = self.mapper.to(NameEnum).map(SourceEnum.VALUE3, model_factory=lambda x: NameEnum[x.name])
        value_enum = self.mapper.to(SourceEnum).map(ValueEnum.B, model_factory=lambda x: SourceEnum(x.value))

        self.assertEqual(name_enum, NameEnum.VALUE3)
        self.assertEqual(value_enum, SourceEnum.VALUE2)


    def test_map__with_registered_constructor_factory(self):
        self.mapper.add(Decimal, ValueObject, model_factory=ValueObject) # pyright: ignore[reportArgumentType]

        self.assertEqual(self.mapper.map(Decimal("42")).value, ValueObject(42).value)


    def test_map__with_constructor_factory(self):
        result = self.mapper.to(ValueObject).map(Decimal("42"), model_factory=ValueObject) # pyright: ignore[reportArgumentType]

        print(result)
        self.assertEqual(result.value, ValueObject(42).value)


    def test_map__with_factory_and_fields_mapping_raises_error(self):
        self.mapper.add(
            ValueEnum,
            ValueObject,
            model_factory=lambda s: ValueObject(int(s.value)),
            fields_mapping={"value": lambda x: x.value}
        )

        with pytest.raises(ValueError):
            self.mapper.map(ValueEnum.A)
