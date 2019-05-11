TARGET ?=
TEST_PATH ?=
export AWS_DEFAULT_REGION=us-east-1

default: all

lint:
	pipenv run pylint src
	# test/**/*.py

unit:
	pipenv run python -m pytest --cov=src test/unit$(TEST_PATH) -W ignore::DeprecationWarning

doc:
	pipenv run python -m pydoc src/example.py

all: lint unit

ifeq (test,$(firstword $(MAKECMDGOALS)))
  # use the rest as arguments for "run"
  RUN_ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
  # ...and turn them into do-nothing targets
  $(eval $(RUN_ARGS):;@:)
endif

test:
	make unit TEST_PATH=/test_$(RUN_ARGS).py

.PHONY: test doc mock lint unit
