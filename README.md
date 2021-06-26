# py-automapper
Python object auto mapper

TODO:
* use https://docs.readthedocs.io/en/stable/index.html


Requirements:
```python
from automapper import mapper

mapper.register_cls_extractor(ParentClassA, fields_name_extractor_function)

mapper.add(SourceClass, TargetClass)

# output type is known from registered before
mapper.map(obj)

# output type specified
mapper.to(TargetClass).map(obj)

# TODO: extra mappings, they override default mapping from `obj`
mapper.map(obj, field1=value1, field2=value2)

# TODO: same extra mappings with specific type, field1 and field2 coming from SpecificType
mapper.map(obj, SpecificType, field1=value1, field2=value2)

# Don't map None values, by default skip_none_values == False
mapper.map(obj, skip_none_values = True)

# TODO: Mapping should be recursive
# TODO: Add optional dependencies for 

# TODO: Advanced: multiple from classes
mapper.add(FromClassA, FromClassB, ToClassC)

# TODO: Advanced: add custom mappings for fields
mapper.add(ClassA, ClassB, {"ClassA.field1", "ClassB.field2", "ClassA.field2", "ClassB.field1"})

# TODO: Advanced: map multiple objects to output type
mapper.multimap(obj1, obj2)
mapper.to(TargetType).multimap(obj1, obj2)

# TODO: Advanced: Verify correctness of all mappings and if it's possible to construct object

```