.DEFAULT_GOAL:=help

.EXPORT_ALL_VARIABLES:

ifndef VERBOSE
.SILENT:
endif

# set default shell
SHELL=/usr/bin/env bash -o pipefail -o errexit

TAG ?= $(shell cat TAG)
POETRY_HOME ?= ${HOME}/.local/share/pypoetry
POETRY_BINARY ?= $(shell command -v poetry 2>/dev/null || echo "${POETRY_HOME}/venv/bin/poetry")
POETRY_VERSION ?= 1.3.2

help:  ## Display this help
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n"} /^[a-zA-Z0-9_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

.PHONY: show-version
show-version:  ## Display version
	echo -n "${TAG}"

.PHONY: build
build: ## Build my-fastapi-project package
	echo "[build] Build my-fastapi-project package."
	${POETRY_BINARY} build

.PHONY: install
install:  ## Install my-fastapi-project with poetry
	@build/install.sh

.PHONY: image
image:  ## Build my-fastapi-project image
	@build/image.sh

.PHONY: metrics
metrics: install ## Run my-fastapi-project metrics checks
	echo "[metrics] Run my-fastapi-project PEP 8 checks."
	${POETRY_BINARY} run flake8 --select=E,W,I --max-line-length 88 --import-order-style pep8 --statistics --count my_fastapi_project
	echo "[metrics] Run my-fastapi-project PEP 257 checks."
	${POETRY_BINARY} run flake8 --select=D --ignore D301 --statistics --count my_fastapi_project
	echo "[metrics] Run my-fastapi-project pyflakes checks."
	${POETRY_BINARY} run flake8 --select=F --statistics --count my_fastapi_project
	echo "[metrics] Run my-fastapi-project code complexity checks."
	${POETRY_BINARY} run flake8 --select=C901 --statistics --count my_fastapi_project
	echo "[metrics] Run my-fastapi-project open TODO checks."
	${POETRY_BINARY} run flake8 --select=T --statistics --count my_fastapi_project tests
	echo "[metrics] Run my-fastapi-project black checks."
	${POETRY_BINARY} run black --check my_fastapi_project

.PHONY: unit-test
unit-test: install ## Run my-fastapi-project unit tests
	echo "[unit-test] Run my-fastapi-project unit tests."
	${POETRY_BINARY} run pytest tests/unit

.PHONY: integration-test
integration-test: install ## Run my-fastapi-project integration tests
	echo "[unit-test] Run my-fastapi-project integration tests."
	${POETRY_BINARY} run pytest tests/integration

.PHONY: coverage
coverage: install  ## Run my-fastapi-project tests coverage
	echo "[coverage] Run my-fastapi-project tests coverage."
	${POETRY_BINARY} run pytest --cov=my_fastapi_project --cov-fail-under=90 --cov-report=xml --cov-report=term-missing tests

.PHONY: test
test: unit-test integration-test  ## Run my-fastapi-project tests

.PHONY: docs
docs: install ## Build my-fastapi-project documentation
	echo "[docs] Build my-fastapi-project documentation."
	${POETRY_BINARY} run sphinx-build docs site

.PHONY: mypy
mypy: install  ## Run my-fastapi-project mypy checks
	echo "[mypy] Run my-fastapi-project mypy checks."
	${POETRY_BINARY} run mypy my_fastapi_project
