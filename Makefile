
all:
	

run:
	uv run --active python3 -m src
clean:
	find . -type d -name __pycache__ -exec rm -rf {} +

install:

	uv venv ~/goinfre/.venv && \
	@echo 'Run: "source .venv/bin/activate" to access the virtual environment.' \
	@echo 'Run: "uv sync --active --cache-dir ~/goinfre/call_me_maybe_cache" to install cache and dependencies'

