PYTHON=python3

.PHONY: test, venv

test:
	PYTHONPATH=. $(PYTHON) -m pytest

.PHONY: venv
venv:
	$(PYTHON) -m venv env
