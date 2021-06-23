# py-automapper
Python object auto mapper

TODO:
* setup mypy, black, flake8
* use pipenv for dependencies or requirements.txt?
* use setup.py for package generation?
* use custom exception type
* use pytest for unit testing

Requirements:
```python
from pyautomapper import mapper

mapper.register(ParentClassA, fields_name_extractor_function)

mapper.add(ClassA, ClassB)

# Advanced feature: multiple from classes
mapper.add(FromClassA, FromClassB, ToClassC)

# add custom mappings for fields
mapper.add(ClassA, ClassB, {"ClassA.field1", "ClassB.field2", "ClassA.field2", "ClassB.field1"})

# output type is known from registered before
mapper.map(obj)

# output type specified
mapper.map(obj, SpecificType)

# extra mappings, they override default mapping from `obj`
mapper.map(obj, field1=value1, field2=value2)

# same extra mappings with specific type, field1 and field2 comming from SpecificType
mapper.map(obj, SpecificType, field1=value1, field2=value2)

# don't map None values, by default skip_none_values == False
mapper.map(obj, skip_none_values = True)

# Advance features
# map multiple objects to output type
mapper.multimap(obj1, obj2)
# or
mapper.multimap(obj1, obj2, SpecificType)

# Verify correctness of all mappings?? That it's possible to construct object


# Alternatives
mapper.to(SpecificType).map(obj, field1=value1, field2=value2, skip_none_values=True)
mapper.to(SpecifitType).map(obj1, obj2, field1=value1)
# I like this more, cause it's more flexible regarding multimap option
# and it may provide better type safety checks, specifically for extra fields, need to check.

```