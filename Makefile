.PHONY: all init clean

PYTHON_DIST = 'pythonw2.7'
PIP_DIST = 'pip-2.7'

all: clean
	$(PYTHON_DIST) server.py

init:
	$(PIP_DIST) install -r requirements.txt

clean:
	rm -rf dist *egg*
