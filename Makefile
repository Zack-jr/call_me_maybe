
all:
	

clean:
	rm -rf __pycache__/

install:

	uv venv ~/goinfre/.venv && \
	uv sync --active --cache-dir ~/goinfre/call_me_maybe_cache
	@echo 'Run: "source .venv/bin/activate" to access the virtual environment.'

