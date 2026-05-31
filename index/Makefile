.PHONY: test lint clean build install

test:
	python -m pytest tests/ -v

lint:
	ruff check latex_index/

fmt:
	ruff format latex_index/

typecheck:
	mypy latex_index/ --strict

clean:
	rm -rf __pycache__ latex_index/__pycache__ tests/__pycache__
	rm -rf .pytest_cache .mypy_cache .ruff_cache
	rm -rf dist build *.egg-info

build:
	python -m build

install:
	pip install -e .

all: lint test
