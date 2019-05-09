export AWS_DEFAULT_REGION=us-east-1

default: test

lint:
	pipenv run pylint src test/**/*.py

unit:
	pipenv run python -m pytest --cov=src test/unit -W ignore::DeprecationWarning

test: lint unit


.PHONY: test
