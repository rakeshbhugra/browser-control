ENV_NAME = browser-control
MINICONDA_PATH = /Users/$(USER)/miniconda3
PYTHON_VERSION = 3.12

install:
	/bin/bash -c '\
	source $(MINICONDA_PATH)/etc/profile.d/conda.sh; \
	if ! conda info --envs | grep -q "^$(ENV_NAME)[[:space:]]"; then \
		echo "Creating conda environment: $(ENV_NAME)"; \
		conda create -y -n $(ENV_NAME) python=$(PYTHON_VERSION); \
	fi; \
	conda activate $(ENV_NAME); \
	pip install -r requirements.txt; \
	playwright install; \
	'
