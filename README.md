<img src="logo.png" align="left" style="width:128px; margin-right: 20px;" />

# py-automapper

**Version**
1.0.1

**Author**
anikolaienko

**Copyright**
anikolaienko

**License**
The MIT License (MIT)

**Last updated**
5 Jan 2022

**Package Download**
https://pypi.python.org/pypi/py-automapper

**Build Status**
TODO

---

## Versions
Check [CHANGELOG.md](/CHANGELOG.md)

## About

**Python auto mapper** is useful for multilayer architecture which requires constant mapping between objects from separate layers (data layer, presentation layer, etc).

Inspired by: [object-mapper](https://github.com/marazt/object-mapper)

The major advantage of py-automapper is its extensibility, that allows it to map practically any type, discover custom class fields and customize mapping rules. Read more in [documentation](https://anikolaienko.github.io/py-automapper).

## Usage
Install package:
```bash
pip install py-automapper
```

Simple mapping:
```python
from automapper import mapper

class SourceClass:
    def __init__(self, name: str, age: int, profession: str):
        self.name = name
        self.age = age
        self.profession = profession

class TargetClass:
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age

# Register mapping
mapper.add(SourceClass, TargetClass)

source_obj = SourceClass("Andrii", 30, "software developer")

# Map object
target_obj = mapper.map(source_obj)

# or one time mapping without registering in mapper
target_obj = mapper.to(TargetClass).map(source_obj)

print(f"Name: {target_obj.name}; Age: {target_obj.age}; has profession: {hasattr(target_obj, 'profession')}")

# Output:
# Name: Andrii; age: 30; has profession: False
```

## Override fields
If you want to override some field and/or add mapping for field not existing in SourceClass:
```python
from typing import List
from automapper import mapper

class SourceClass:
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age

class TargetClass:
    def __init__(self, name: str, age: int, hobbies: List[str]):
        self.name = name
        self.age = age
        self.hobbies = hobbies

mapper.add(SourceClass, TargetClass)

source_obj = SourceClass("Andrii", 30)
hobbies = ["Diving", "Languages", "Sports"]

# Override `age` and provide missing field `hobbies`
target_obj = mapper.map(source_obj, age=25, hobbies=hobbies)

print(f"Name: {target_obj.name}; Age: {target_obj.age}; hobbies: {target_obj.hobbies}")
# Output:
# Name: Andrii; Age: 25; hobbies: ['Diving', 'Languages', 'Sports']

# Modifying initial `hobbies` object will not modify `target_obj`
hobbies.pop()

print(f"Hobbies: {hobbies}")
print(f"Target hobbies: {target_obj.hobbies}")

# Output:
# Hobbies: ['Diving', 'Languages']
# Target hobbies: ['Diving', 'Languages', 'Sports']
```

## Extensions
`py-automapper` has few predefined extensions for mapping to classes for frameworks:
* [FastAPI](https://github.com/tiangolo/fastapi) and [Pydantic](https://github.com/samuelcolvin/pydantic)
* [TortoiseORM](https://github.com/tortoise/tortoise-orm)

When you first time import `mapper` from `automapper` it checks default extensions and if modules are found for these extensions, then they will be automatically loaded for default `mapper` object.

What does extension do? To know what fields in Target class are available for mapping `py-automapper` need to extract the list of these fields. There is no generic way to do that for all Python objects. For this purpose `py-automapper` uses extensions.

List of default extensions can be found in [/automapper/extensions](/automapper/extensions) folder. You can take a look how it's done for a class with `__init__` method or for Pydantic or TortoiseORM models.

You can create your own extension and register in `mapper`:
```python
from automapper import mapper

class TargetClass:
    def __init__(self, **kwargs):
        self.name = kwargs["name"]
        self.age = kwargs["age"]
    
    @staticmethod
    def get_fields(cls):
        return ["name", "age"]

source_obj = {"name": "Andrii", "age": 30}

try:
    # Map object
    target_obj = mapper.to(TargetClass).map(source_obj)
except Exception as e:
    print(f"Exception: {repr(e)}")
    # Output:
    # Exception: KeyError('name')

    # mapper could not find list of fields from BaseClass
    # let's register extension for class BaseClass and all inherited ones
    mapper.add_spec(TargetClass, TargetClass.get_fields)
    target_obj = mapper.to(TargetClass).map(source_obj)

    print(f"Name: {target_obj.name}; Age: {target_obj.age}")
```

You can also create your own clean Mapper without any extensions and define extension for very specific classes, e.g. if class accepts `kwargs` parameter in `__init__` method and you want to copy only specific fields. Next example is a bit complex but probably rarely will be needed:
```python
from typing import Type, TypeVar

from automapper import Mapper

# Create your own Mapper object without any predefined extensions
mapper = Mapper()

class TargetClass:
    def __init__(self, **kwargs):
        self.data = kwargs.copy()

    @classmethod
    def fields(cls):
        return ["name", "age", "profession"]

source_obj = {"name": "Andrii", "age": 30, "profession": None}

try:
    target_obj = mapper.to(TargetClass).map(source_obj)
except Exception as e:
    print(f"Exception: {repr(e)}")
    # Output:
    # Exception: MappingError("No spec function is added for base class of <class 'type'>")

# Instead of using base class, we define spec for all classes that have `fields` property
T = TypeVar("T")

def class_has_fields_property(target_cls: Type[T]) -> bool:
    return callable(getattr(target_cls, "fields", None))
    
mapper.add_spec(class_has_fields_property, lambda t: getattr(t, "fields")())

target_obj = mapper.to(TargetClass).map(source_obj)
print(f"Name: {target_obj.data['name']}; Age: {target_obj.data['age']}; Profession: {target_obj.data['profession']}")
# Output:
# Name: Andrii; Age: 30; Profession: None

# Skip `None` value
target_obj = mapper.to(TargetClass).map(source_obj, skip_none_values=True)
print(f"Name: {target_obj.data['name']}; Age: {target_obj.data['age']}; Has profession: {hasattr(target_obj, 'profession')}")
# Output:
# Name: Andrii; Age: 30; Has profession: False
```
