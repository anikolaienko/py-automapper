1.2.3 - 2022/11/21
* Added automated code checks for different Python versions.

1.2.2 - 2022/11/20
* [@soldag] Fixed mapping of string enum types [#17](https://github.com/anikolaienko/py-automapper/pull/17)

1.2.1 - 2022/11/13
* Fixed dictionary source mapping to target object.
* Implemented CI checks

1.2.0 - 2022/10/25
* [@g-pichler] Ability to disable deepcopy on mapping: `use_deepcopy` flag in `map` method.
* [@g-pichler] Improved error text when no spec function exists for `target class`.
* Updated doc comments.

1.1.3 - 2022/10/07
* [@g-pichler] Added support for SQLAlchemy models mapping
* Upgraded code checking tool and improved code formatting

1.0.4 - 2022/07/25
* Added better description for usage with Pydantic and TortoiseORM
* Improved type support

1.0.3 - 2022/07/24
* Fixed issue with dictionary collection: https://github.com/anikolaienko/py-automapper/issues/4

1.0.2 - 2022/07/24
* Bug fix: pass parameters override in MappingWrapper.map
* Added support for mapping fields with different names: https://github.com/anikolaienko/py-automapper/issues/3

1.0.1 - 2022/01/05
* Bug fix

1.0.0 - 2022/01/05
* Finalized documentation, fixed defects

0.1.1 - 2021/07/18
* No changes, set version as Alpha

0.1.0 - 2021/07/18
* Implemented base functionality

0.0.1 - 2021/06/23
* Initial version