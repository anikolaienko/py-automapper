# Contribution guide <!-- omit in toc -->
Any contribution is welcome. If you noticed a bug or have a feature idea create a new Issue in [Github Issues](https://github.com/anikolaienko/py-automapper/issues). For small fixes it's enough to create PR with description.

Table of Contents:
- [Dev environment](#dev-environment)
- [Pre-commit](#pre-commit)
- [Run tests](#run-tests)

# Dev environment
* Install prerequisites from `dev-requirements.txt`:
```bash
pip install -r dev-requirements.txt
```
* Install `py-automapper` dependencies with poetry:
```bash
poetry install
```

# Pre-commit
This project is using `pre-commit` checks to format and verify code. Same checks are used on CI as well. Activate `pre-commit` for your local setup:
```bash
pre-commit install
```
After this code checks will run on `git commit` command.

If some of the `pre-commit` dependencies are not found make sure to activate appropriate poetry virtualenv. To check path to virtual environment run:
```bash
poetry env info -p
```

Or run pre-commit manually:
```
poetry run pre-commit run --all-files
```

# Run tests
To run unit tests use command:
```
poetry run pytest tests/
```
