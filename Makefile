.PHONY: build debug test coverage clean annotate all


PYTHON ?= python


all: build


clean:
	rm -rf dist build *.egg-info
	find . -name '__pycache__' | xargs rm -rf
	rm -rf htmlcov
	rm -rf __tnt*


build:
	$(PYTHON) setup.py build


test:
	PYTHONASYNCIODEBUG=1 $(PYTHON) -m unittest discover -v -s tests
	$(PYTHON) -m unittest discover -v -s tests
	USE_UVLOOP=1 $(PYTHON) -m unittest discover -v -s tests


quicktest:
	$(PYTHON) -m unittest discover -v -s tests


test_16:
	TARANTOOL_DOCKER_VERSION=1.6 $(PYTHON) -m unittest discover -s tests


test_17:
	TARANTOOL_DOCKER_VERSION=1.7 $(PYTHON) -m unittest discover -s tests


coverage:
	# pip install -e .
	coverage run run_tests.py
	coverage report -m
	coverage html


style:
	pep8 asynctnt_queue
	pep8 tests


sdist: clean build test
	$(PYTHON) setup.py sdist


release: clean build test
	$(PYTHON) setup.py sdist upload


docs: build
	$(MAKE) -C docs html
