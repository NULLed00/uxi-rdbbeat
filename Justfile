export UV_INDEX_STRATEGY := "unsafe-best-match"

PYTHON_VERSION := "3.11"

# Show this message and exit.
help:
	@just --list

# Clean temporary files from repo folder
clean:
	rm -rf build dist wheels *.egg-info
	rm -rf */build */dist
	find . -path '*/__pycache__/*' -delete
	find . -type d -name '__pycache__' -empty -delete
	rm -rf '.mypy_cache'
	rm -rf '.pytest_cache'
	rm -rf '.coverage'
	rm -rf '.ruff_cache'
	rm -rf '.coverage.*'

# Install uv
install-uv:
	pip install --quiet --upgrade uv

# Setup Python virtual environment
setup-python: install-uv
	uv python install {{PYTHON_VERSION}}
	uv venv -p {{PYTHON_VERSION}}

# Create requirements.txt file
requirements: install-uv
	uv pip compile --universal --no-strip-extras dev-requirements.in --output-file=dev-requirements.txt

requirements-upgrade:
    uv pip compile --upgrade --universal --no-strip-extras dev-requirements.in --output-file=dev-requirements.txt

# Setup requirements
setup: install-uv
	uv pip install -e .

# Setup dev requirements
setup-dev:
	uv pip sync dev-requirements.txt
	uv pip install -e .

# Auto-format the code
fmt:
	uv run ruff check --fix --exit-zero
	uv run ruff check --select I --fix --exit-zero
	uv run ruff format
	uv run python -m tools.yaml-sorter fmt

# Run all lints
lint:
	uv run ruff format --check
	uv run ruff check --select I
	uv run ruff check
	uv run basedpyright .
	uv run yamllint .
	uv run python -m tools.yaml-sorter lint

test-setup:
	echo "No test setup."

# Run tests
test +ARGS='':
	uv run coverage run -m pytest {{ARGS}}

# Create coverage report
coverage:
	uv run coverage xml
	uv run coverage report

# Server version bump using bumpversion (major, minor, patch)
bumpversion +ARGS='':
	bumpversion --config-file .bumpversion.cfg {{ARGS}}
