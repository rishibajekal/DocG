.PHONY: all init setup cleanup clean

all: clean
	`which python` server.py

init:
	`which pip` install -r requirements.txt

setup: cleanup
	`which python` setup.py

cleanup:
	`which python` cleanup.py

clean:
	rm -rf dist *egg*
