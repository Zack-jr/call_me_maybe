all:
	clear
	export HF_HOME=~/goinfre/call_me_maybe_cache && uv run --active python -m src

run:
	export HF_HOME=~/goinfre/call_me_maybe_cache && uv run --active python -m src

install:

	uv venv ~/goinfre/.venv
	@echo 'Run: "source ~/goinfre/.venv/bin/activate" to access the virtual environment.'
	@echo 'Run: "uv sync --active --cache-dir ~/goinfre/call_me_maybe_cache" to install cache and dependencies'

debug:
	export HF_HOME=~/goinfre/call_me_maybe_cache && uv run --active python -m pdb -m src

clean:

	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf .mypy_cache

lint:
	uv run --active flake8 .
	uv run --active mypy . --warn-return-any \
	--warn-unused-ignores --ignore-missing-imports \
	--disallow-untyped-defs --check-untyped-defs


.PHONY: all install run debug clean lint