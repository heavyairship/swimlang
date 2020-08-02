# FixMe: add full README.md
# FixMe: add simplfmt to format .sl files

PYTHON = /usr/bin/python3

clean:
	rm -rf __pycache__ *.pyc simple_lang/__pycache__ simple_lang/*pc build/ dist/ simple_lang.egg-info

install:
	pip3 install . --user
	cp simple_lang/simpl.py /usr/local/bin/simpl
	cp simple_lang/simplfmt.py /usr/local/bin/simplfmt

uninstall:
	pip3 uninstall -y simple_lang
	rm /usr/local/bin/simpl
	rm /usr/local/bin/simplfmt

check: clean uninstall install
	(echo "\nrunning test.py" && $(PYTHON) tests/test.py && \
	echo "\nrunning test.sl" && simpl examples/test.sl --verbose && \
	echo "\nrunning factorial.sl" && simpl examples/factorial.sl --verbose && \
	echo "\nrunning log_2.sl" && simpl examples/log_2.sl --verbose && \
	echo "\nrunning higher_order.sl" && simpl examples/higher_order.sl --verbose && \
	echo "\nrunning factorial_rec.sl" && simpl examples/factorial_rec.sl --verbose && \
	echo "\nrunning call_test.sl" && simpl examples/call_test.sl --verbose && \
	echo "\nrunning list_example.sl" && simpl examples/list_example.sl --verbose && \
	echo "\nrunning maps.sl" && simpl examples/maps.sl --verbose && \
	echo "\ntests passed") || (echo "\ntests failed")
	
play: clean install
	simpl playground.sl --verbose
