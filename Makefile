.PHONY: test
test: nose lint

nose:
	nosetests --with-coverage

lint:
	pylint gzippy
	pycodestyle gzippy
	pydocstyle gzippy
	flake8 gzippy

install:
	python setup.py install

requirements:
	pip freeze | grep -v gzippy > requirements.txt
