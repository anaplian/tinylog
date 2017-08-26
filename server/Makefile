# Makefile for tinylog_server
all: run

rebuild_venv:
	rm -rf venv
	make venv

venv:
	test -d venv || virtualenv venv
	venv/bin/pip3 install -Ur requirements.txt
	venv/bin/pip3 install -Ur dev_requirements.txt

run: venv
	@echo "Running tinylog_server..."
	@scripts/run

check: test

test: venv
	@venv/bin/python3 -m nose -s

acceptance_test: venv
	@make db
	@venv/bin/behave acceptance_tests

lint: venv
	@venv/bin/python3 -m pylint ./tinylog_server/*.py

db:
	@rm -f dev.db
	@/bin/bash -c "PYTHONPATH=$$PYTHONPATH:$$(pwd p) ./scripts/create_db"
