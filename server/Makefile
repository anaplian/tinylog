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
	@FLASK_APP=tinylog_server/app.py venv/bin/flask run --host=0.0.0.0 --port=8000

check: test

test: venv
	@venv/bin/python3 -m nose -s

acceptance_test: venv
	@venv/bin/behave acceptance_tests

lint: venv
	@venv/bin/python3 -m pylint ./tinylog_server/*.py

