# FixMe: organize this repo properly with setup.py, etc.
# FixMe: add README.md

PYTHON = /usr/bin/python3

check:
	echo "\nrunning test.py" && $(PYTHON) test.py && \
	echo "\nrunning test.sl" && $(PYTHON) simple_lang.py test.sl --verbose && \
	echo "\nrunning factorial.sl" && $(PYTHON) simple_lang.py factorial.sl --verbose && \
	echo "\nrunning log_2.sl" && $(PYTHON) simple_lang.py log_2.sl --verbose && \
	echo "\nrunning higher_order.sl" && $(PYTHON) simple_lang.py higher_order.sl --verbose && \
	echo "\nrunning factorial_rec.sl" && $(PYTHON) simple_lang.py factorial_rec.sl --verbose && \
	echo "\nrunning list_example.sl" && $(PYTHON) simple_lang.py list_example.sl --verbose

clean:
	rm -rf __pycache__ *.pyc