.PHONY: clean clean-test clean-pyc clean-build docs help
.DEFAULT_GOAL := help

PACKAGE=watchmagic

define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT

help:
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

clean: clean-build clean-pyc clean-test ## remove all build, test, coverage and Python artifacts

clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

style: ## style code using isort & black, then check style using flake8
	isort $(PACKAGE)/*.py
	isort $(PACKAGE)/tests/*.py
	black $(PACKAGE)
	flake8 $(PACKAGE) 

style-check: ## check code style using isort & black, then check style using flake8
	isort -c $(PACKAGE)/*.py
	isort -c $(PACKAGE)/tests/*.py
	black --check $(PACKAGE)
	flake8 $(PACKAGE) 

test: ## run tests quickly with the default Python
	pytest

test-all: ## run tests on every Python version with tox
	tox

release: dist ## package and upload a release
	twine upload dist/*

dist: clean ## builds source and wheel package
	python setup.py sdist
	python setup.py bdist_wheel
	ls -l dist
