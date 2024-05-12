help:
	@echo  "Py-Automapper development makefile"
	@echo
	@echo  "usage: make <target>"
	@echo  "Targets:"
	@echo  "    clean   Clean all the cache in repo directory"
	@echo  "    install Ensure dev/test dependencies are installed"
	@echo  "    test    Run all tests"
	@echo  "    docs    [not-working] Builds the documentation"
	@echo  "    build   Build into a package (/dist folder)"
	@echo  "    publish Publish the package to pypi.org"

clean:
	rm -rf build dist .mypy_cache .pytest_cache .coverage py_automapper.egg-info

install:
	pip install .[dev]
	pip install .[test]

test:
	pytest

build:
	python -m build

publish:
	twine publish

docs: install
	rm -fR ./build
	sphinx-build -M html docs build
