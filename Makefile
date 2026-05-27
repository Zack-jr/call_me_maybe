
all:
	

install:

	python3 -m venv ~/goinfre/.venv && \
	. ~/goinfre/.venv/bin/activate && \
	uv sync --active --cache-dir ~/goinfre/call_me_maybe_cache
