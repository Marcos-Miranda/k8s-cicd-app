lint:
	black app/ tests/
	flake8 app/ tests/
	mypy app/ tests/

test: 
	pytest

lint-test: lint test

