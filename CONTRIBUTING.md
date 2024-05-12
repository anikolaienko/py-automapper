# Contribution guide <!-- omit in toc -->
Any contribution is welcome. If you noticed a bug or have a feature idea create a new Issue in [Github Issues](https://github.com/anikolaienko/py-automapper/issues). For small fixes it's enough to create PR with description.

Table of Contents:
- [Dev environment](#dev-environment)
- [Pre-commit](#pre-commit)
- [Run tests](#run-tests)

# Dev environment
* Install all dependencies:
```bash
pip install .[dev]
pip install .[test]
```

# Pre-commit
This project is using `pre-commit` checks to format and verify code. Same checks are used on CI as well. Activate `pre-commit` for your local setup:
```bash
pre-commit install
```
After this code checks will run on `git commit` command.

If some of the `pre-commit` dependencies are not found make sure to activate appropriate virtual environment

To run `pre-commit` manually use:
```bash
pre-commit run --all-files
```

# Run tests
To run unit tests use command:
```bash
make test
```
or simply
```bash
pytest
```
