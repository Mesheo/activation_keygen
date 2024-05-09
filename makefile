ruff_fix:
	ruff check --fix src

ruff_check:
	ruff check src

mypy_check:
	mypy src

requirements_dev:
	pip install .
