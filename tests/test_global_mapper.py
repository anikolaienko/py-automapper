from unittest import TestCase

from automapper import mapper as global_mapper


class ParentClass:
    def __init__(self, num: int, text: str) -> None:
        self.num = num
        self.text = text


class ChildClass(ParentClass):
    def __init__(self, num: int, text: str, flag: bool) -> None:
        super().__init__(num, text)
        self.flag = flag


class AnotherClass:
    def __init__(self, text: str, num: int) -> None:
        self.text = text
        self.num = num


# Test class
class GlobalMapperTest(TestCase):
    def test_to__produces_wrapper_for_mapping(self):
        source_obj = ChildClass(10, "test_text", False)

        result = global_mapper.to(AnotherClass).map(source_obj)

        assert isinstance(result, AnotherClass)
        assert result.text == "test_text"
