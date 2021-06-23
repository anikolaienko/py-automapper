from typing import Type, Iterable
from unittest import TestCase

import automapper.mapper as mapper


## Test data
class ParentClass:
    def __init__(self, num: int, text: str) -> None:
        self.num = num
        self.text = text

class ChildClass(ParentClass):
    def __init__(self, num: int, text: str, flag: bool) -> None:
        super().__init__(num, text)
        self.flag = flag

def custom_fields_extractor(concrete_class: Type) -> Iterable[str]:
    fields = []
    for val_name, val_type in concrete_class.__init__.__annotations__.items():
        if val_name != 'return':
            fields.append(val_name)
    return fields


## Test class
class AutomapperTest(TestCase):
    def test_register_extractor__adds_to_internal_collection(self):
        try:
            mapper.register_extractor(ParentClass, custom_fields_extractor)
            assert ParentClass in mapper.__FIELD_EXTRACTORS__
            assert ["num", "text", "flag"] == mapper.__FIELD_EXTRACTORS__[ParentClass](ChildClass)
        finally:
            mapper.__FIELD_EXTRACTORS__.clear()
