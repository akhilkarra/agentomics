.PHONY: env tests lock-conda clean tests docs data
.DEFAULT_GOAL := tests
env:
	@echo "Setting up environment with uv..."
	uv venv
	uv sync --extra dev --extra test
	pre-commit install
	uv run pre-commit run --all-files
	@echo "Done!"

clean:
	@echo "Removing environment..." && \
	rm -rf .venv
	@echo "Done!"

format:
	@echo "Formatting files..." && \
	uv run ruff check --fix
	@echo "Done!"

test:
	@echo "Running tests..." && \
	uv run pytest -v
	@echo "Done!"

test-integration:
	@echo "Running ONLY INTEGRATION tests..." && \
	uv run pytest -m "integration" -v
	@echo "Done!"

test-non-integration:
	@echo "Running ONLY NON-INTEGRATION tests..." && \
	uv run pytest -m "not integration" -v
	@echo "Done!"

reference-docs:
	@echo "Creating documentation..." && \
	uv run pdoc agentomics --output-dir docs/api --force
	@echo "Done!"

data:
	@echo "IMPORTANT: Please make sure you activate your environment before running this target.\nSetting up Data Version Control (DVC)..." && \
	dvc get https://github.com/iterative/dataset-registry \
          get-started/data.xml -o data/data.xml --force
	@echo "Done!"

create-books:
	@echo "Creating jupyter-book books..."
	uv run jupyter-book create docs
	@echo "Done!"

books:
	@echo "Building jupyter-book books..."
	uv run jupyter-book build docs
	@echo "Done!"

publish:
	@echo "Publishing jupyter-book books..."
	uv run ghp-import -n -p -f docs/_build/html
	@echo "Done!"
