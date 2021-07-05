# py-automapper
Python object auto mapper

Current mapper can be useful for multilayer architecture which requires constant mapping between objects from separate layers (data layer, presentation layer, etc).

For more information read the [documentation](https://anikolaienko.github.io/py-automapper).

## Usage example:
```python
from automapper import mapper

# Add automatic mappings
mapper.add(SourceClass, TargetClass)

# Map object of SourceClass to output object of TargetClass
mapper.map(obj)

# Map object to AnotherTargetClass not added to mapping collection
mapper.to(AnotherTargetClass).map(obj)

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
mapper.register_cls_extractor(
    BaseClass,
    lambda child_class: child_class.get_fields_function()
)

# Add your own extension for extracting list of fields from class
# for all classes that can be identified in verification function
mapper.register_fn_extractor(
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
