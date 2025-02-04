from collections import OrderedDict
from dataclasses import dataclass

from automapper import mapper


@dataclass
class Teacher:
    teacher: str


class Student:
    def __init__(self, name: str, classes: dict[str, Teacher]):
        self.name = name
        self.classes = classes
        self.ordered_classes = OrderedDict(classes)


class PublicUserInfo:
    def __init__(
        self,
        name: str,
        classes: dict[str, Teacher],
        ordered_classes: dict[str, Teacher],
    ):
        self.name = name
        self.classes = classes
        self.ordered_classes = ordered_classes


def test_map__dict_and_ordereddict_are_mapped_correctly_to_same_types():
    classes = {"math": Teacher("Ms G"), "art": Teacher("Mr A")}
    student = Student("Tim", classes)

    public_info = mapper.to(PublicUserInfo).map(student)

    assert public_info.name is student.name

    assert public_info.classes == student.classes
    assert public_info.classes is not student.classes
    assert isinstance(public_info.classes, dict)

    assert public_info.ordered_classes == student.ordered_classes
    assert public_info.ordered_classes is not student.ordered_classes
    assert isinstance(public_info.ordered_classes, OrderedDict)
