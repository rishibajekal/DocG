.PHONY: all init clean

all: clean
	`which python` server.py

init:
	`which pip` install -r requirements.txt

clean:
	rm -rf dist *egg*
