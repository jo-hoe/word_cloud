include help.mk

ROOT_DIR := $(dir $(realpath $(lastword $(MAKEFILE_LIST))))
VENV_DIR :=${ROOT_DIR}.venv
SCRIPT_DIR := ${VENV_DIR}/Scripts/

.DEFAULT_GOAL := start

.PHONY: init
init: venv update ## init setup of project after checkout

.PHONY: venv
venv:
	@python -m venv ${VENV_DIR}

.PHONY: pull
pull:
	@git -C ${ROOT_DIR} pull

.PHONY: update
update: pull ## pulls git repo and installs all dependencies
	${SCRIPT_DIR}pip install -r ${ROOT_DIR}requirements.txt

.PHONY: save-dependencies
save-dependencies: ## save current dependencies
	"${ROOT_DIR}.venv/Scripts/pip" list --not-required --format=freeze | grep -v "pip" > ${ROOT_DIR}requirements.txt

.PHONY: test
test: ## run all tests
	${SCRIPT_DIR}python -m unittest discover -s $(ROOT_DIR)test/ --verbose
