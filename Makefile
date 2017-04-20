VIRTUALENV = virtualenv
SPHINX_BUILDDIR = docs/_build
VENV := $(shell echo $${VIRTUAL_ENV-.venv})
PYTHON = $(VENV)/bin/python
DEV_STAMP = $(VENV)/.dev_env_installed.stamp
INSTALL_STAMP = $(VENV)/.install.stamp
TEMPDIR := $(shell mktemp -d)

.IGNORE: clean
.PHONY: all install virtualenv tests tests-once tests-integration

OBJECTS = .venv .coverage

all: install
install: $(INSTALL_STAMP)

$(INSTALL_STAMP): $(PYTHON) setup.py
	$(VENV)/bin/pip install -U -e .
	touch $(INSTALL_STAMP)

install-dev: install $(DEV_STAMP)
$(DEV_STAMP): $(PYTHON) dev-requirements.txt
	$(VENV)/bin/pip install -r dev-requirements.txt
	touch $(DEV_STAMP)

virtualenv: $(PYTHON)
$(PYTHON):
	virtualenv $(VENV)
	$(VENV)/bin/pip install --upgrade pip


tests-once: install-dev
	$(VENV)/bin/py.test \
		--cov-config .coveragerc \
		--cov-report term-missing \
		--cov-fail-under 100 --cov ipreputation

tests:
	tox

tests-integration: install-dev
	$(PYTHON) tests/test_client.py

clean:
	find . -name '*.pyc' -delete
	find . -name '__pycache__' -type d -exec rm -fr {} \;

build-requirements:
	$(VIRTUALENV) $(TEMPDIR)
	$(TEMPDIR)/bin/pip install -U pip
	$(TEMPDIR)/bin/pip install -Ue .
	$(TEMPDIR)/bin/pip freeze | egrep -v "^-e" > requirements.txt
