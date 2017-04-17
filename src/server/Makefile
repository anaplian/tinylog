# Makefile for TinyLog
all: run

rebuild_venv:
	rm -rf venv
	make venv

venv:
	test -d venv || virtualenv venv
	venv/bin/pip3 install -Ur requirements.txt
	venv/bin/pip3 install -Ur dev_requirements.txt

run: venv
	@echo "Running TinyLog Server..."
	venv/bin/python3 tinylogserver/manage.py runserver

check: test

test: venv
	@venv/bin/python3 tinylogserver/manage.py test tinylogserver/api/tests

lint: venv
	@venv/bin/pylint ./tinylogserver/**/*.py
