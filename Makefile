# FixMe: organize this repo properly with setup.py, etc.
# FixMe: add README.md

PYTHON = /usr/bin/python3

check:
	$(PYTHON) test.py && $(PYTHON) simple_lang.py --file test.sl --verbose

clean:
	rm -rf __pycache__ *.pyc