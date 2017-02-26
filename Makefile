PACKAGE_NAME	:= p4rr0t007
VERSION		:= 0.1.3
export VERSION
export PACKAGE_NAME

.PHONY: tests dist docs

all: clean pip tests

pip:
	@pip install --disable-pip-version-check --no-cache-dir -U pip
	@pip install -r development.txt

tests:
	@nosetests tests

clean:
	@find . -name '*.pyc' -delete
	@echo "version = '${VERSION}'" > p4rr0t007/version.py

docs:
	cd docs && make linkcheck html


build: clean docs
	python setup.py sdist
	@cd dist && tar xzvf dist/${PACKAGE_NAME}-${VERSION}.tar.gz

release: tests build
	-@twine register -r d4v1ncy dist/${PACKAGE_NAME}-${VERSION}.tar.gz
	@twine upload -r d4v1ncy dist/${PACKAGE_NAME}-${VERSION}.tar.gz
	@rm -rf *egg-info* dist/${PACKAGE_NAME}-${VERSION}.tar.gz
