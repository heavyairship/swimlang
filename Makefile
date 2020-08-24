# FixMe: add full README.md

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

lint:
	simplfmt examples/log_2.sl && \
	simplfmt examples/call_test.sl && \
	simplfmt examples/factorial.sl && \
	simplfmt examples/factorial_rec.sl && \
	simplfmt examples/higher_order.sl && \
	simplfmt examples/list_example.sl && \
	simplfmt examples/test.sl && \
	simplfmt examples/bst.sl && \
	simplfmt examples/maps.sl && \
	simplfmt examples/map_reduce.sl && \
	simplfmt examples/fizz_buzz.sl && \
	simplfmt examples/times_table.sl

check: clean uninstall install
	$(MAKE) lint
	(echo "\nrunning test.py" && $(PYTHON) tests/test.py && \
	echo "\nrunning test.sl" && simpl examples/test.sl --verbose && \
	echo "\nrunning factorial.sl" && simpl examples/factorial.sl --verbose && \
	echo "\nrunning log_2.sl" && simpl examples/log_2.sl --verbose && \
	echo "\nrunning higher_order.sl" && simpl examples/higher_order.sl --verbose && \
	echo "\nrunning factorial_rec.sl" && simpl examples/factorial_rec.sl --verbose && \
	echo "\nrunning call_test.sl" && simpl examples/call_test.sl --verbose && \
	echo "\nrunning list_example.sl" && simpl examples/list_example.sl --verbose && \
	echo "\nrunning maps.sl" && simpl examples/maps.sl --verbose && \
	echo "\nrunning fizz_buzz.sl" && simpl examples/fizz_buzz.sl --verbose && \
	echo "\nrunning map_reduce.sl" && simpl examples/map_reduce.sl --verbose && \
	echo "\nrunning bst.sl" && simpl examples/bst.sl --verbose && \
	echo "\nrunning bst.sl" && simpl examples/times_table.sl --verbose && \
	echo "\ntests passed") || (echo "\ntests failed")
	
play: clean install
	simpl playground.sl --verbose
