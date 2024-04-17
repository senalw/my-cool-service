WORKING_DIR=$(shell pwd)

.PHONY: setup
venv:
	python3 -m venv venv
	./venv/bin/python3 -m pip install --upgrade pip

.PHONY: install
install: venv
	./venv/bin/pip3 install -r requirements.txt

clean:
	rm -rf venv

create-reports-dir:
	mkdir -p reports

.PHONY: setup-style
setup-style: setup
	./venv/bin/pip3 install --no-cache-dir -r requirements-style.txt
	./venv/bin/pre-commit install --hook-type pre-commit --hook-type pre-push

.PHONY: setup-test
setup-test: setup
	./venv/bin/pip3 install -r requirements-test.txt

.PHONY: check-format
check-format: # Check which files will be reformatted
	./venv/bin/black --check .

.PHONY: format
format: # Format files
	./venv/bin/black .

.PHONY: lint-py
lint-py:
	./venv/bin/flake8 .

.PHONY: lint-py-ci
lint-py-ci: create-reports-dir
	./venv/bin/flake8 . > reports/flake8.log

.PHONY: lint
lint:
	$(MAKE) lint-py

.PHONY: setup-dev
setup-dev: setup setup-test setup-style

run:
	PYTHONPATH=./src: ./venv/bin/python src/main.py
