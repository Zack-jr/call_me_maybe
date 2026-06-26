
all:
	
run:
	export HF_HOME=~/goinfre/call_me_maybe_cache && uv run --active python -m src
clean:
	find . -type d -name __pycache__ -exec rm -rf {} +

install:

	uv venv ~/goinfre/.venv && \
	@echo 'Run: "source ~/goinfre/.venv/bin/activate" to access the virtual environment.' \
	@echo 'Run: "uv sync --active --cache-dir ~/goinfre/call_me_maybe_cache" to install cache and dependencies'

