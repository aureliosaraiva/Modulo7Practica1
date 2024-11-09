create-env:
	python3 -m venv .

clean-env:
	rm -rf .pytest_cache catalog_overview.egg-info lib bin

use-env:
	pip3 install -e .

install:
	pip3 install -r requirements.txt
test:
	pytest tests -s

lint:
	flake8 src tests cmd
