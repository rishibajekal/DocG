.PHONY: all init setup cleanup clean

all: clean
	`which python` server.py

init:
	`which pip` install -r requirements.txt

setup: cleanup
	python setup.py

cleanup:
	python cleanup.py

clean:
	rm -rf dist *egg*
