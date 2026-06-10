.PHONY: install sample demo test lint check

install:
	python -m pip install -e ".[dev]"

sample:
	python tools/generate_sample.py

demo:
	python examples/quickstart.py

test:
	pytest tests/ -v

lint:
	ruff check src/ tests/ examples/ tools/

check: sample demo lint test