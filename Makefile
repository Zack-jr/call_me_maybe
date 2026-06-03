
all:
	

install:

	python3 -m venv ~/goinfre/.venv && \
	uv sync --active --cache-dir ~/goinfre/call_me_maybe_cache
	@echo 'Run: "source .venv/bin/activate" to access the virtual environment.'

