# Environment variables 
PYTHON_INTERPRETER = python
PIP = $(PYTHON_INTERPRETER) -m pip
WD = $(shell pwd)
PYTHONPATH = ${WD}
SHELL := /bin/bash

## define our activate venv command
define activate_venv
    source venv/bin/activate && $1
endef

create-virtual-environment:
	@echo ">>> Setting up the virtualEnv. <<<"
	$(PYTHON_INTERPRETER) -m venv venv
	@echo ">>> Setting up the virtualEnv was completed"

## 'call' is used as we're working in a shell, need to activate venv with each entry
## adding, but may not use
## requirements.in are more flexible, we may not need this flexibility, yet: $(call activate_venv, pip-compile requirements.in)
install-requirements: create-virtual-environment
	@echo ">>> Installing requirements <<<"
	$(call activate_venv, $(PIP) install pip-tools)
	$(call activate_venv, $(PIP) install -r ./requirements.txt)
	@echo ">>> Finished installing requirements <<<"

## Install bandit for security checks
bandit:
	$(call activate_venv, $(PIP) install bandit)

## Install black PEP8 guidelines
black:
	$(call activate_venv, $(PIP) install black)

## Install coverage for showing details on what code was run and which code was not - refactoring?
coverage:
	$(call activate_venv, $(PIP) install pytest-cov)

## Set up dev requirements (bandit, black & coverage)
dev-setup: create-virtual-environment bandit black coverage

## Run the security test (bandit) on all directories and the parent directory
security-test:
	$(call activate_venv, bandit -lll */*.py *c/*/*.py)

## Run the black code check
run-black:
	$(call activate_venv, black ./src/*.py ./test/*.py  ./utility/*.py)

## Run the unit tests
unit-test:
	$(call activate_venv, PYTHONPATH=${PYTHONPATH} pytest -vv)

## Run the coverage check - we might not make use of this but leaving
check-coverage:
	$(call activate_venv, PYTHONPATH=${PYTHONPATH} pytest --cov=src test/)

run-all: install-requirements security-test run-black unit-test check-coverage