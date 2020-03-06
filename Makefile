PIPENV_PYTHON_VERSION  ?= 3.6


.PHONY: all
all:
	$(error please pick a target)

.PHONY: upload
upload: clean build
	pipenv run upload

.PHONY: build
build:
	pipenv run build

.PHONY: clean
clean:
	rm -rf dist build nuclio_sdk.egg-info

.PHONY: clean_pyc
clean_pyc:
	find . -name '*.pyc' -exec rm {} \;

.PHONY: flake8
flake8:
	pipenv run flake8

.PHONY: test
test:
	pipenv run test

.PHONY: install_pipenv
install_pipenv:
	python -m pip install --user pipenv
	python -m pipenv --python ${PYTHON_VERSION}
ifeq ($(PIPENV_PYTHON_VERSION), 2.7)
	pipenv install -r requirements.py2.txt
else
	pipenv install --dev
endif
