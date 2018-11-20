#!/usr/bin/make

NAME="Kafka_Python"


PYTHON=python
COVERAGE=coverage
REPORT_DIR="report"
PYTEST_OPTS = --cov=$(NAME) --junitxml $(REPORT_DIR)/pytest.xml --cov-report html:$(REPORT_DIR)/coverage/index.html

FLAKE8_IGNORE = E302,E203,E261

all: clean check flake8 pylint tests

flake8:
	flake8 --ignore=$(FLAKE8_IGNORE) $(NAME)/
	flake8 --ignore=$(FLAKE8_IGNORE),E402 tests/

pylint:
	find $(NAME) ./tests -name \*.py -not -path "./venv/*"| xargs pylint3 --rcfile .pylintrc

clean:
	@echo "Cleaning up distutils stuff"
	rm -rf build
	rm -rf dist
	rm -rf MANIFEST
	rm -rf *.egg-info
	@echo "Cleaning up byte compiled python stuff"
	find . -type f -regex ".*\.py[co]$$" -delete
	@echo "Cleaning up doc builds"
	rm -rf docs/_build
	rm -rf docs/api_modules
	rm -rf docs/client_modules
	@echo "Cleaning up test reports"
	rm -rf report/*

tests: unittest systest coverage_report

unittest: clean
	py.test $(PYTEST_OPTS) tests/unit/* 

systest: clean
	py.test $(PYTEST_OPTS) tests/system/*

coverage_report:
	$(COVERAGE) report --rcfile=".coveragerc"