checkfiles = automapper/ tests/
black_opts = -l 100 -t py37
py_warn = PYTHONDEVMODE=1

help:
	@echo  "Py-Automapper development makefile"
	@echo
	@echo  "usage: make <target>"
	@echo  "Targets:"
	@echo  "    update  Updates dev/test dependencies"
	@echo  "    install Ensure dev/test dependencies are installed"
	@echo  "    style   Auto-formats the code"
	@echo  "    check	Auto-fomats and then checks the code"
	@echo  "    test	Runs all tests"
	@echo  "    build   Produces dist/ package folder"
	@echo  "    publish Publishes package to repository"
	@echo  "    docs 	[Not-Implemented] Builds the documentation"
	

update:
	@poetry update

install:
	@poetry install

style: install
	black $(black_opts) $(checkfiles)

check: install style
	flake8 $(checkfiles)
	mypy $(checkfiles)

test:
	@poetry run pytest

build: install
	rm -fR dist/
	@poetry build

publish: install
	@poetry publish

docs: install
	rm -fR ./build
	sphinx-build -M html docs build
