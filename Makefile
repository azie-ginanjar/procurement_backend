clean:
	find . -type f -name "*.pyc" -exec rm {} \;

develop:
	python setup.py develop

install:
	python setup.py install
