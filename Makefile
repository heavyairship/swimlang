PYTHON = /usr/bin/python3

check:
	$(PYTHON) test.py && $(PYTHON) simple_lang.py --file test.sl 

clean:
	rm -rf __pycache__ *.pyc