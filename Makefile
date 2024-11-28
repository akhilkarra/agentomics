.PHONY: env tests lock-conda clean tests docs data
.DEFAULT_GOAL := tests
# If CONDA variable is not defined, create it
CONDA?=${CONDA_PREFIX}
env_name = agentomics
python_version = 3.11.5

env:
	@echo "Setting up environment..."
	conda create --name $(env_name) --channel conda-forge --no-default-packages python=$(python_version) conda-lock && \
	. ${CONDA}/etc/profile.d/conda.sh && \
	conda activate $(env_name) && \
	conda-lock install --name $(env_name) conda-lock.yml && \
	poetry lock && poetry install && \
	pre-commit install && \
	poetry run pre-commit run --all-files
	@echo "Done!"

lock-conda:
	. ${CONDA}/etc/profile.d/conda.sh && \
	conda activate $(env_name) && \
	conda-lock -f environment.yaml

clean:
	@echo "Removing environment..." && \
	conda remove --name $(env_name) --all
	@echo "Done!"

poetry-dev:
	poetry add jupyter pre-commit --group dev

poetry-test:
	poetry add pytest --group test

poetry: poetry-dev poetry-test
	poetry add numpy scipy pandas scikit-learn nltk matplotlib

format:
	@echo "Formatting files..." && \
	. ${CONDA}/etc/profile.d/conda.sh && \
	conda activate $(env_name) && \
	poetry run ruff check --fix
	@echo "Done!"

test:
	@echo "Running tests..." && \
	. ${CONDA}/etc/profile.d/conda.sh && \
	conda activate $(env_name) && \
	poetry run pytest -v
	@echo "Done!"

test-integration:
	@echo "Running ONLY INTEGRATION tests..." && \
	. ${CONDA}/etc/profile.d/conda.sh && \
	conda activate $(env_name) && \
	poetry run pytest -m "integration" -v
	@echo "Done!"

test-non-integration:
	@echo "Running ONLY NON-INTEGRATION tests..." && \
	. ${CONDA}/etc/profile.d/conda.sh && \
	conda activate $(env_name) && \
	poetry run pytest -m "not integration" -v
	@echo "Done!"

reference-docs:
	@echo "Creating documentation..." && \
	. ${CONDA}/etc/profile.d/conda.sh && \
	conda activate $(env_name) && \
	poetry run pdoc agentomics -o docs/api --force
	@echo "Done!"

# . ${CONDA}/etc/profile.d/conda.sh && \
# conda activate $(env_name) && \

data:
	@echo "IMPORTANT: Please make sure you activate your environment before running this target.\nSetting up Data Version Control (DVC)..." && \
	dvc get https://github.com/iterative/dataset-registry \
          get-started/data.xml -o data/data.xml --force
	@echo "Done!"

create-books:
	@echo "Creating jupyter-book books..."
	. ${CONDA}/etc/profile.d/conda.sh && \
	conda activate $(env_name) && \
	poetry run jupyter-book create docs
	@echo "Done!"

books:
	@echo "Building jupyter-book books..."
	. ${CONDA}/etc/profile.d/conda.sh && \
	conda activate $(env_name) && \
	poetry run jupyter-book build docs
	@echo "Done!"

publish:
	@echo "Publishing jupyter-book books..."
	. ${CONDA}/etc/profile.d/conda.sh && \
	conda activate $(env_name) && \
	ghp-import -n -p -f docs/_build/html
	@echo "Done!"
