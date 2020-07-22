# FixMe: organize this repo properly with setup.py, etc.
# FixMe: add README.md

PYTHON = /usr/bin/python3

check:
	$(PYTHON) test.py && \
	$(PYTHON) simple_lang.py test.sl --verbose && \
	$(PYTHON) simple_lang.py factorial.sl --verbose && \
	$(PYTHON) simple_lang.py log_2.sl --verbose && \
	$(PYTHON) simple_lang.py higher_order.sl --verbose

clean:
	rm -rf __pycache__ *.pyc