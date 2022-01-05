<img src="logo.png" align="left" style="width:128px; margin-right: 20px;" />

# py-automapper

**Version**
1.1.0

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
    name: str
    age: int
    profession: str

class TargetClass:
    name: str
    age: int

# Register mapping
mapper.add(SourceClass, TargetClass)

source_obj = SourceClass("Andrii", 30, "software developer")

# Map object
target_obj = mapper.map(obj)

print(target_obj)
```

One time mapping without registering in mapper:
```python
target_obj = mapper.to(TargetClass).map(source_obj)
```

```python
# Override specific fields or provide missing ones
mapper.map(obj, field1=value1, field2=value2)

# Don't map None values to target object
mapper.map(obj, skip_none_values = True)
```

## Advanced features
```python
from automapper import Mapper

# Create your own Mapper object without any predefined extensions
mapper = Mapper()

# Add your own extension for extracting list of fields from class
# for all classes inherited from base class
mapper.add_spec(
    BaseClass,
    lambda child_class: child_class.get_fields_function()
)

# Add your own extension for extracting list of fields from class
# for all classes that can be identified in verification function
mapper.add_spec(
    lambda cls: hasattr(cls, "get_fields_function"),
    lambda cls: cls.get_fields_function()
)
```
For more information about extensions check out existing extensions in `automapper/extensions` folder

## Not yet implemented features
```python

# TODO: multiple from classes
mapper.add(FromClassA, FromClassB, ToClassC)

# TODO: add custom mappings for fields
mapper.add(ClassA, ClassB, {"Afield1": "Bfield1", "Afield2": "Bfield2"})

# TODO: Advanced: map multiple objects to output type
mapper.multimap(obj1, obj2)
mapper.to(TargetType).multimap(obj1, obj2)
```
